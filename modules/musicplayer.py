import asyncio
import discord
import time
from discord.ext import commands
from discord.utils import find
import tools.checks as checks
import tools.discordembed as dmbd
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.parse as urlparse
import requests

def PutInFront(arr, var):
    url_data = urlparse.urlparse(var)
    query = urlparse.parse_qs(url_data.query)
    vcode = query["v"][0]
    e=0
    for y in arr:
        if vcode in y:
            del arr[e]
            arr.insert(0, var)
            break
        e+=1
    return arr

def getPlaylistLinks(url):
    linklist = []
    if "www.youtube.com" in url and "playlist" in url:
        sourceCode = requests.get(url).text
        soup = BeautifulSoup(sourceCode, 'html.parser')
        domain = 'https://www.youtube.com'
        for link in soup.find_all("a", {"dir": "ltr"}):
            href = link.get('href')
            if href.startswith('/watch?'):
                linklist.append(domain + href)
    elif "www.youtube.com" in url and "list" in url:
        url_data = urlparse.urlparse(url)
        query = urlparse.parse_qs(url_data.query)
        playlistcode = query["list"][0]
        vimg = "https://www.youtube.com/playlist?list={}".format(playlistcode)
        linklist = getPlaylistLinks(vimg)
        linklist = PutInFront(linklist, url)
    elif "www.youtube.com" not in url:
        query = urllib.parse.quote(url)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
            if "watch?" in vid['href']:
                linklist.append('https://www.youtube.com' + vid['href'])
                break
    else:
        linklist = [url]

    return linklist

Client = discord.Client()
client = commands.Bot(command_prefix = "d!")

class QueueEntry:
    def __init__(self, player):
        self.player = player

    def __str__(self):
        fmt = '{0.title}'
        duration = self.player.duration
        if duration:
            fmt = fmt + '|{0[0]}m {0[1]}s'.format(divmod(duration, 60))
        return fmt.format(self.player)

class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = '{0.title}|{0.uploader}'
        duration = self.player.duration
        if duration:
            fmt = fmt + '|{0[0]}m {0[1]}s'.format(divmod(duration, 60))
        return fmt.format(self.player)


class VoiceState:
    def __init__(self, client):
        self.current = None
        self.voice = None
        self.client = client
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue(maxsize=100)
        self.songlist = []
        self.songnamelist = []
        self.skip_votes = set()  # a set of user_ids that voted
        self.audio_player = self.client.loop.create_task(self.audio_player_task())
        self.loopactive = False
        self.songmessage = None
        self.songchannel = None
        self.IsStopped = False

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def stop(self):
        try:
            self.audio_player.cancel()
            del self.voice_states[self.serverid]
            self.voice.disconnect()
        except:
            pass


    def toggle_next(self):
        self.client.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            if not self.IsStopped:
                self.play_next_song.clear()
                self.current = await self.songs.get()
                try:
                    em = dmbd.playerembed(self.current.player)
                    m = await self.client.send_message(self.current.channel, embed=em)
                except Exception as e:
                    pass
                await self.client.add_reaction(m, "⏯")
                await self.client.add_reaction(m, "⏩")
                await self.client.add_reaction(m, "🔁")
                await self.client.add_reaction(m, "🔂")
                if self.loopactive:
                    try:
                        channel = self.client.get_channel(self.songchannel)
                        msg = await self.client.get_message(channel, self.songmessage)
                        opts = {
                            'default_search': 'auto',
                            'quiet': True,
                            'noplaylist': True,
                        }
                        player = await self.voice.create_ytdl_player(self.songlist[0], ytdl_options=opts, after=self.toggle_next)
                        self.songlist.append(self.songlist[0])
                        player.volume = 0.3
                        entry = VoiceEntry(msg, player)
                        qentry = QueueEntry(player)
                        self.songnamelist.append(str(qentry))
                        await self.songs.put(entry)
                    except Exception as e:
                        pass
                del self.songlist[0]
                del self.songnamelist[0]
                self.current.player.start()
                await self.play_next_song.wait()


class Music:
    """Voice related commands.
    Works in multiple servers at once.
    """
    def __init__(self, client):
        self.client = client
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.client)
            self.voice_states[server.id] = state

        return state

    def CreateNewState(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.client)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.client.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.client.loop.create_task(state.voice.disconnect())
            except:
                pass

    @client.event
    async def on_reaction_add(self, reaction, user):
        try:
            if user.voice_channel.id in [y.channel.id for y in self.client.voice_clients]:
                if reaction.message.author.id == self.client.user.id:
                    if str(reaction.emoji) == "⏯" and not user.id == "402246509313392640" and not reaction.message.author.id == user.id:
                        state = self.get_voice_state(reaction.message.server)
                        if state.is_playing():
                            player = state.player
                            player.pause()
                    elif str(reaction.emoji) == "⏩" and not user.id == "402246509313392640" and not reaction.message.author.id == user.id:
                        state = self.get_voice_state(reaction.message.server)
                        if not state.is_playing():
                            await self.client.send_message(reaction.message.channel, 'Not playing any music right now...')
                            return
                        voter = user
                        if voter == state.current.requester or len(state.current.requester.voice_channel.voice_members) < 4:
                            await self.client.send_message(reaction.message.channel, 'Requester requested skipping song...')
                            state.skip()
                        elif voter.id not in state.skip_votes:
                            state.skip_votes.add(voter.id)
                            total_votes = len(state.skip_votes)
                            if total_votes >= 2:
                                await self.client.send_message(reaction.message.channel, '**⏩ Skip vote passed, skipping song now**')
                                state.skip()
                            else:
                                await self.client.send_message(reaction.message.channel, 'Skip vote added, currently at [{}/3]'.format(total_votes))
                        else:
                            await self.client.send_message(reaction.message.channel, '⛔ You have already voted to skip this song.')
                    elif str(reaction.emoji) == "🔁" and not user.id == "402246509313392640" and not reaction.message.author.id == user.id:
                        state = self.get_voice_state(reaction.message.server)
                        if not state.loopactive:
                            state.loopactive = True
                            opts = {
                                'default_search': 'auto',
                                'quiet': True,
                                'noplaylist': True,
                            }
                            player = await state.voice.create_ytdl_player(state.songlist[0], ytdl_options=opts, after=state.toggle_next)
                            player.volume = 0.3
                            state.songlist.append(state.songlist[0])
                            state.songmessage = reaction.message.id
                            state.songchannel = reaction.message.channel.id
                            entry = VoiceEntry(reaction.message, player)
                            qentry = QueueEntry(player)
                            state.songnamelist.append(str(qentry))
                            msg = ("Playlist Looping Started.")
                            em = dmbd.musicembed(msg)
                            await self.client.send_message(reaction.message.channel, embed=em)
                            await state.songs.put(entry)
                    elif str(reaction.emoji) == "🔂" and not user.id == "402246509313392640" and not reaction.message.author.id == user.id:
                        state = self.get_voice_state(reaction.message.server)
                        if not state.loopactive:
                            opts = {
                                'default_search': 'auto',
                                'quiet': True,
                                'noplaylist': True,
                            }
                            player = await state.voice.create_ytdl_player(state.songlist[0], ytdl_options=opts, after=state.toggle_next)
                            player.volume = 0.3
                            if state.songlist[0] != state.songlist[-1] or len(state.songlist) == 1:
                                state.songlist.append(state.songlist[0])
                                state.songmessage = reaction.message.id
                                state.songchannel = reaction.message.channel.id
                                entry = VoiceEntry(reaction.message, player)
                                qentry = QueueEntry(player)
                                state.songnamelist.append(str(qentry))
                                msg = ("Readded song to playlist.")
                                em = dmbd.musicembed(msg)
                                await self.client.send_message(reaction.message.channel, embed=em)
                                await state.songs.put(entry)
        except Exception as e:
            pass
    @client.event
    async def on_reaction_remove(self, reaction, user):
        try:
            if user.voice_channel.id in [y.channel.id for y in self.client.voice_clients]:
                if reaction.message.author.id == self.client.user.id:
                    if str(reaction.emoji) == "⏯" and not user.id == "402246509313392640" and not reaction.message.author.id == user.id:
                        state = self.get_voice_state(reaction.message.server)
                        if state.is_playing():
                            player = state.player
                            player.resume()
                    elif str(reaction.emoji) == "🔁" and not user.id == "402246509313392640" and not reaction.message.author.id == user.id:
                        state = self.get_voice_state(reaction.message.server)
                        state.loopactive = False
                        msg = ("Stopped looping playlist.")
                        em = dmbd.musicembed(msg)
                        await self.client.send_message(reaction.message.channel, embed=em)
        except Exception as e:
            pass


    @commands.command(pass_context=True, no_pm=True)
    async def join(self, ctx, *, channel: discord.Channel):
        """Joins a voice channel."""
        try:
            await self.create_voice_client(channel)
        except discord.ClientException:
            await self.client.say('Already in a voice channel...')
        except discord.InvalidArgument:
            await self.client.say('This is not a voice channel...')
        else:
            await self.client.say('Ready to play audio in ' + channel.name)

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        """Summons the client to join your voice channel."""
        summoned_channel = ctx.message.author.voice_channel
        summoned_server = ctx.message.server.id
        if summoned_channel is None:
            await self.client.say('You are not in a voice channel.')
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.client.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)
        return True

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song : str):
        """Plays a song.
        If there is a song currently in the queue, then it is
        queued until the next song is done playing.
        This command automatically searches as well from YouTube.
        The list of supported sites can be found here:
        https://rg3.github.io/youtube-dl/supportedsites.html
        """
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
            'noplaylist': True,
        }
        e = False
        for y in self.client.voice_clients:
            if y.server == ctx.message.server:
                state.voice = y
                e = True


        if state.voice is None:
            if e:
                success = True
            else:
                success = await ctx.invoke(self.summon)
            if not success:
                return
        linklist = getPlaylistLinks(song)
        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.client.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            if len(linklist) == 1:
                song = linklist[0]
                try:
                    player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
                    state.IsStopped = False
                    if ctx.message.author.voice_channel.id in [y.channel.id for y in self.client.voice_clients]:
                        print(player.duration)
                        if player.duration <= 3600:
                            if "earrape" in (player.title).lower():
                                player.volume = 0.05
                            else:
                                player.volume = 0.3
                            entry = VoiceEntry(ctx.message, player)
                            if len(state.songlist) == 0:
                                state.songlist.append(song)
                            state.songlist.append(song)
                            qentry = QueueEntry(player)
                            state.songnamelist.append(str(qentry))
                            state.message = ctx.message
                            await self.client.say('**Added** `{} by {}` **to the queue.**'.format((str(entry).split("|"))[0], (str(entry).split("|"))[1]))
                            await state.songs.put(entry)
                        elif checks.checkvip(ctx.message):
                            if "earrape" in (player.title).lower():
                                player.volume = 0.05
                            else:
                                player.volume = 0.3
                            entry = VoiceEntry(ctx.message, player)
                            if len(state.songlist) == 0:
                                state.songlist.append(song)
                            state.songlist.append(song)
                            qentry = QueueEntry(player)
                            state.songnamelist.append(str(qentry))
                            state.message = ctx.message
                            await self.client.say('**Added** `{} by {}` **to the queue.**'.format((str(entry).split("|"))[0], (str(entry).split("|"))[1]))
                            await state.songs.put(entry)
                        else:
                            msg="Only Donators can enqueue a song longer than **1 hour**."
                            em = dmbd.musicembed(msg)
                            await self.client.say(embed=em)
                except Exception as e:
                    fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
                    await self.client.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
            else:
                await self.client.say("**Playlist found**")
                for song in linklist:
                    try:
                        player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
                        state.IsStopped = False
                        if ctx.message.author.voice_channel.id in [y.channel.id for y in self.client.voice_clients]:
                            if player.duration <= 3600:
                                if "earrape" in (player.title).lower():
                                    player.volume = 0.05
                                else:
                                    player.volume = 0.3
                                entry = VoiceEntry(ctx.message, player)
                                if len(state.songlist) == 0:
                                    state.songlist.append(song)
                                state.songlist.append(song)
                                qentry = QueueEntry(player)
                                state.songnamelist.append(str(qentry))
                                state.message = ctx.message
                                await state.songs.put(entry)
                            elif checks.checkvip(ctx.message):
                                if "earrape" in (player.title).lower():
                                    player.volume = 0.05
                                else:
                                    player.volume = 0.3
                                entry = VoiceEntry(ctx.message, player)
                                if len(state.songlist) == 0:
                                    state.songlist.append(song)
                                state.songlist.append(song)
                                qentry = QueueEntry(player)
                                state.songnamelist.append(str(qentry))
                                state.message = ctx.message
                                await state.songs.put(entry)
                            else:
                                await self.client.say("**Only Donators can enqueue a song longer than `1 hour`.**")
                            time.sleep(0.5)
                    except Exception as e:
                        fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
                        await self.client.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
                await self.client.say("**Playlist Added**")



    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value: int):
        """Sets the volume of the currently playing song."""
        if ctx.message.author.voice_channel.id in [y.channel.id for y in self.client.voice_clients]:
            state = self.get_voice_state(ctx.message.server)
            if state.is_playing():
                if value > 200 or value < 1:
                    await self.client.say('Value too high! 1 - 200 only!')
                    return
                player = state.player

                player.volume = value / 100
                await self.client.say('Set the volume to {:.0%}'.format(player.volume))


    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        """Pauses the currently played song."""
        if ctx.message.author.voice_channel.id in [y.channel.id for y in self.client.voice_clients]:
            state = self.get_voice_state(ctx.message.server)
            if state.is_playing():
                player = state.player
                player.pause()


    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        """Resumes the currently played song."""
        if ctx.message.author.voice_channel.id in [y.channel.id for y in self.client.voice_clients]:
            state = self.get_voice_state(ctx.message.server)
            if state.is_playing():
                player = state.player
                player.resume()

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        """Stops playing audio and leaves the voice channel.
        This also clears the queue.
        """
        server = ctx.message.server
        state = self.get_voice_state(server)

        if state.is_playing():
            player = state.player

            try:
                state.IsStopped = True
                state.player.pause()
                time.sleep(1)
                state.audio_player.cancel()
                state.player.stop()
                del self.voice_states[server.id]
            except:
                pass
        e=0
        time.sleep(1)
        for x in self.client.voice_clients:
            state = self.get_voice_state(x.server)
            if state.is_playing():
                e+=1
        y = []
        if e == 0:
            for x in self.client.voice_clients:
                y.append(x)
            for a in y:
                await a.disconnect()





    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        """Vote to skip a song. The song requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """
        if ctx.message.author.voice_channel.id in [y.channel.id for y in self.client.voice_clients]:

            state = self.get_voice_state(ctx.message.server)
            if not state.is_playing():
                await self.client.say('Not playing any music right now...')
                return

            voter = ctx.message.author
            if voter == state.current.requester:
                state.skip()
            elif voter.id not in state.skip_votes:
                state.skip_votes.add(voter.id)
                total_votes = len(state.skip_votes)
                if total_votes >= 3:
                    await self.client.say('**⏩ Skip vote passed, skipping song now**')
                    state.skip()
                else:
                    await self.client.say('Skip vote added, currently at [{}/3]'.format(total_votes))
            else:
                await self.client.say('⛔ You have already voted to skip this song.')


    @commands.command(pass_context=True, no_pm=True)
    async def isplaying(self, ctx):
        """Shows info about the currently played song."""

        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.client.say('Not playing anything.')
        else:
            skip_count = len(state.skip_votes)
            await self.client.say('Now playing {} [skips: {}/3]'.format(state.current, skip_count))

    @commands.command(pass_context=True, no_pm=True)
    async def loop(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.client.say('Not playing anything.')
        else:
            if not state.loopactive:
                state.loopactive = True
                opts = {
                    'default_search': 'auto',
                    'quiet': True,
                    'noplaylist': True,
                }
                player = await state.voice.create_ytdl_player(state.songlist[0], ytdl_options=opts, after=state.toggle_next)
                player.volume = 0.3
                state.songlist.append(state.songlist[0])
                state.songmessage = ctx.message.id
                state.songchannel = ctx.message.channel.id
                entry = VoiceEntry(ctx.message, player)
                qentry = QueueEntry(player)
                state.songnamelist.append(str(qentry))
                msg = ("Playlist Looping Started.")
                em = dmbd.musicembed(msg)
                await self.client.say(embed=em)
                await state.songs.put(entry)
            else:
                state.loopactive = False
                msg = ("Playlist Looping Stopped.")
                em = dmbd.musicembed(msg)
                await self.client.say(embed=em)


    @commands.command(pass_context=True, no_pm=True)
    async def queue(self, ctx, page=None):
        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            msg = "Queue is empty"
        elif page == None:
            msg = ""
            e = 0
            for y in state.songnamelist:
                if e != 10 and (len(msg) + len(y) + 5) < 1950:
                    e+=1
                    msg = msg + "\n**{}.** {}".format(e, y)
                else:
                    return
        else:
            msg = ""
            e = 0
            page = (page*10)-10
            try:
                for y in state.songnamelist[page:]:
                    if e != 10 and (len(msg) + len(y) + 5) < 1950:
                        e+=1
                        msg = msg + "\n**{}.** {}".format(e, y)
                    else:
                        return
            except:
                msg = "No such page!"
        if state.loopactive and msg != "":
            msg = "**LOOPING**\n" + msg
        em = dmbd.musicembed(msg)
        await self.client.say(embed=em)



def setup(client):
    client.add_cog(Music(client))
