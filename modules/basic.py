import asyncio
import time
import random
import discord
import wikipedia
import sys
import os
from mtranslate import translate
import datetime
import r6sapi as api
from cleverwrap import CleverWrap
from discord.ext import commands
import tools.checks as checks
from discord.ext.commands import Bot
import tools.discordembed as dmbd
import tools.dragonsql as sql
name = "Dragon"


Client = discord.Client()
client = commands.Bot(command_prefix = "d!")
client.remove_command('help')
Purgemax = 31
scriptstart = int(round(time.time()))

class Basic:

    def __init__(self, client):
        self.client = client

    #@commands.command(pass_context=True)
    #async def AmIMaster(self, ctx):
    #        """Check if you are able to controle Dragon"""
    #        for r in ctx.message.author.roles:
    #            if "dragon master" == r.name.lower():
    #                await self.client.say("Yes, You are my master!")
    #                print(UserID, "Has used the bot for:",ctx.message.content)
    #                break
    #        else:
    #            await self.client.say("*Sniff Sniff* YOU ARE NOT MY MASTER")

    @commands.command(pass_context=True)
    async def forcesay(self, ctx, *, themesssage: str):
            """Force Dragon to say something"""
            for r in ctx.message.author.roles:
                if "dragon master" == r.name.lower():
                    UserID = ctx.message.author.id
                    await self.client.delete_message(ctx.message)
                    await self.client.say("This is what <@%s> forced me to say```\n%s\n```" % (UserID, themesssage))
                    UserID = ctx.message.author
                    print(UserID, "Has used the bot for:",ctx.message.content)
                    break

    @commands.command(pass_context=True)
    async def say(self, ctx, *, themesssage: str):
            """Let Dragon say something"""
            for r in ctx.message.author.roles:
                if "dragon master" == r.name.lower():
                    UserID = ctx.message.author.id
                    await self.client.delete_message(ctx.message)
                    await self.client.say(themesssage)
                    UserID = ctx.message.author
                    print(UserID, "Has used the bot for:",ctx.message.content)
                    break

    #@commands.command(pass_context=True)
    #async def kick(self, ctx, user: discord.Member, *, content: str):
    #        """Kick user"""
    #        for r in ctx.message.author.roles:
    #            if "dragon master" == r.name.lower():
    #                reason = content
    #                await self.client.send_message(user, "You have been kicked by **{}** for reason: *{}*".format(ctx.message.author.name, reason))
    #                await self.client.kick(user)
    #                await self.client.say("{} has been kicked by {} for reason: {}".format(content[0], ctx.message.author.name, reason))
    #                await self.client.delete_message(ctx.message)
    #                break

    @commands.command(pass_context=True)
    async def purge(self, ctx, *, clearnumb: int):
            """Purge messages"""
            for r in ctx.message.author.roles:
                if "dragon master" == r.name.lower():
                    if clearnumb >= Purgemax:
                        clearnumb = Purgemax - 1
                    clearnumb += 2
                    await self.client.say("Ok master, I will clear the last %s messages" % (str(clearnumb-2)))
                    time.sleep(2)
                    await self.client.purge_from(channel=ctx.message.channel, limit=clearnumb)
                    UserID = ctx.message.author
                    print(UserID, "Has used the bot for:",ctx.message.content)
                    break

    @commands.command(pass_context=True)
    async def info(self, ctx):
            """Cleaner version of this  <-- More info"""
            title = "**Dragon's info Archive**"
            desc = "***Moderation***\n- d!purge [number] *max 31*\n- d!announce [#channel] [announcement] *Announce something.*\n- d!say [text] *Talk in name of the bot*\n- d!forcesay [text] *Make it look like the bot is a hostage*\n- d!joinc [@channel] *Enables join messsage on that channel*"
            em = dmbd.infopage(title, desc)
            await self.client.send_message(ctx.message.author, embed=em)
            desc = "***Fun***\n- d!chat *Have a nice chat with Dragon*\n- d!ping *Pings the bot*\n- d!rtd *Roll the dice*\n- d!flip *Coin Flip*\n- d!choose [choice1 choice2 choice3...] *Chooses between multiple choices*\n- d!kill [@user] *Kill this user in a random way*\n- d!minigame *Starts a random minigame*\n- d!translate [Language Code] [Text you want to translate] *Translates text*"
            em = dmbd.infop(desc)
            await self.client.send_message(ctx.message.author, embed=em)
            desc = "***Music***\n- d!play *Play the requested song*\n- d!join *Joins a voice channel.*\n- d!summon *Summon d!to join your voice channel*\n- d!pause *Pauses the current song*\n- d!resume *Resumes the current paused song*\n- d!stop *Stops the song queue and makes the bot leave*\n- d!skip *Plays the next song in queue*\n- d!isplaying *Shows the info about the current song*\n- d!queue *Shows Current Music Queue.*"
            em = dmbd.infop(desc)
            await self.client.send_message(ctx.message.author, embed=em)
            desc = "***Info***\n- d!info *this message*\n- d!report Bug *Report a bug (Abusing will result in a ban from Dragon)*\n- d!creds *Check out the Dragon Creds*\n- d!invite *Invite Dragon to your own server*"
            em = dmbd.infop(desc)
            await self.client.send_message(ctx.message.author, embed=em)
            desc = "***Rainbow Six Siege***\n- d!rainbowgeneral [username] [uplay/playstation/xbox] *Check general stats for the given user*\n*More coming soon*"
            em = dmbd.infop(desc)
            await self.client.send_message(ctx.message.author, embed=em)
            desc = "***Economy***\n- d!balcreate *Creates a bank account*\n- d!bal *Shows you your balance*\n- d!leaderboard *Shows the server leaderboard*\n- d!deposit [money] *Deposits the amount of money to your bank*\n- d!withdraw [money] *Withdraws money from your bank*\n- d!crime *Make some illegal money (Can lose money during this)*\n- d!work *Make money legal way*\n- d!mug [@player] *Mugs the player*\n- d!heist *Starts a heist 'start heist' to start it 'join heist' to join one*"
            em = dmbd.infop(desc)
            await self.client.send_message(ctx.message.author, embed=em)
            #desc = "***Fortnite***\n- d!fnsolo [name] [platform] *Shows solo stats of that user*\n- d!fnduo [name] [platform] *Shows duo stats of that user*\n- d!fnsquad [name] [platform] *Shows squad stats of that user*\n"
            #em = dmbd.infop(desc)
            #await self.client.send_message(ctx.message.author, embed=em)
            DMS = await self.client.say("The info has been send to your DM's ;)")
            await self.client.delete_message(ctx.message)
            await asyncio.sleep(5)
            await self.client.delete_message(DMS)

    @commands.command(pass_context=True)
    async def serverinfo(self, ctx):
        server = ctx.message.server


    @commands.command(pass_context=True)
    async def announce(self, ctx, *, content: str):
            """Announce something with Dragon"""
            for r in ctx.message.author.roles:
                if "dragon master" == r.name.lower():
                    author = ctx.message.author
                    contentarr = content.split(" ")
                    channel = contentarr[0]
                    channel = channel.strip('<#>')
                    channel = self.client.get_channel(channel)
                    title = "ANNOUNCEMENT"
                    desc = " ".join(contentarr[1:])
                    em = dmbd.newembed(author, title, desc)
                    await self.client.send_message(channel, embed=em)
                    UserID = ctx.message.author
                    print(UserID, "Has used the bot for:",ctx.message.content)
                    break

    @commands.command(pass_context=True)
    async def servers(self, ctx):
        serveram = len(client.servers)
        print(serveram)
        await self.client.say("I'm currently on",serveram,"servers.")
        await self.client.change_presence(game=discord.Game(name="Active on %s servers" % (serveram), url="https://liamd.pw/", type=3))


    @commands.command(pass_context=True)
    async def ping(self, ctx):
        serveram = len(self.client.servers)
        serermem = 0
        for y in self.client.servers:
            serermem += len(y.members)
        timecheck = int(round(time.time()))
        uptime = round(timecheck - scriptstart)
        hours = uptime // 3600
        uptime %= 3600
        minutes = uptime // 60
        uptime %= 60
        time_then = time.monotonic()
        pinger = await self.client.send_message(ctx.message.channel, '__*`Pinging...`*__')
        ping = '%i' % (1000*(time.monotonic()-time_then)) # you can edit this to say whatever you want really. Hope this helps.
        author = "Pong"
        desc = '**Ping** \n{}ms \n**Servers** \n{} \n**Users** \n{} \n**Created With** \nPython 3.5.3 \n**Uptime** \n{} Hours {} Minutes {} Seconds \n**Version** \nV.3.0.2\n**Invite me**\n[Invite](https://discordapp.com/oauth2/authorize?client_id=402246509313392640&permissions=942927063&scope=bot)'.format(ping, serveram, serermem, hours, minutes, uptime)
        em = dmbd.infopage(author, desc)
        await self.client.delete_message(pinger)
        await self.client.say(embed=em)
        time.sleep(1)
        game = "{} Servers | d!info".format(str(serveram))
        await self.client.change_presence(game=discord.Game(name=game, url="https://liamd.pw/", type=3))

    #@commands.command(pass_context=True)
    #async def wikisearch(self, ctx, *, search: str):
    #    """ Grabs Wikipedia Article """
    #    searchlist = wikipedia.search(search)
    #    if len(searchlist) < 1:
    #        author = ctx.message.author
    #        title = "Searched for: " + search
    #        desc = 'No Results Found'
    #        em = dmbd.newembed(author, title, desc)
    #        await self.client.say(embed=em)
    #    else:
    #        page = wikipedia.page(searchlist[0])
    #        author = ctx.message.author
    #        title = page.title
    #        desc = wikipedia.summary(searchlist[0], 3)
    #        url = page.url
    #        em = dmbd.newembed(author, title, desc, url)
    #        em.set_image(url=page.images[0])
    #        em.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Wikipedia-logo-v2-en.svg/250px-Wikipedia-logo-v2-en.svg.png")
    #        await self.client.say(embed=em)

    @commands.command(pass_context=True)
    async def getmembers(self, ctx):
        members = len(ctx.message.server.members)
        await self.client.say(members)

    @commands.command(pass_context=True)
    async def chat(self, ctx, *, text: str):
        await self.client.send_typing(ctx.message.channel)
        reply = cb.say(text)
        reply = "[" + ctx.message.author.name + "] " + reply
        await self.client.say(reply)

    @commands.command(pass_context=True)
    async def getuser(self, ctx, *, u: str):
        u = u.strip("<@!>")
        u = await self.client.get_user_info(u)
        chan = ctx.message.channel
        em = dmbd.userinfo(u, chan)
        await self.client.say(embed=em)

    #@commands.command(pass_context=True)
    #async def uptime(self, ctx):
    #    timecheck = int(round(time.time()))
    #    uptime = round(timecheck - scriptstart)
    #    hours = uptime // 3600
    #    uptime %= 3600
    #    minutes = uptime // 60
    #    uptime %= 60
    #    await self.client.say("I've been online for {} Hours {} Minutes and {} Seconds".format(hours, minutes, uptime))

    @commands.command(pass_context=True)
    async def kill(self, ctx, *, vic: discord.User):
        kills = ["**`{}` just shot `{}`.** 🔫 ", "**`{}` attached a 💣 under `{}`'s chair.**", "**`{}` just stabbed `{}`.** 🔪", "**`{}` did a duel against `{}` and won.** ⚔️", "`{}` **Set `{}` on Fire.** 🔥", "`{}`** turned `{}` into a frog.** 🐸", "`{}` **used his freeze spell on `{}`.** ❄"]
        rnd = random.randint(0,6)
        msg = kills[rnd].format(ctx.message.author.name, vic.name)
        await self.client.delete_message(ctx.message)
        await self.client.say(msg)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 300, commands.BucketType.server)
    async def minigame(self, ctx):
        minigame = ["Easter Egg Hunt", "Find The Diamond"]
        picked = minigame[random.randint(0,1)]
        await self.client.say("Minigame '{}' starts in 15s".format(picked))
        time.sleep(10)
        if picked == minigame[0]:
            eggfindings = ["🥓", "a 🍪", "a piece of 🍫", "some fake 💰", "a 🗝", "a 💊... Please eat it", "a used 💉", "a 🍓", "the winning 🐣", "a 🍩", "a piece of 🍕"]
            await self.client.say("Minigame started: Type 'Search Egg' untill you found the right one (🐣)")
            found = False

            while found == False:
                eggcheck = await self.client.wait_for_message(content="Search Egg")
                if eggcheck:
                    didwin = random.randint(0,10)
                    if didwin == 8:
                        await self.client.say("<@{}> has found the winning egg {}".format(eggcheck.author.id, eggfindings[didwin]))
                        await self.client.delete_message(eggcheck)
                        found = True
                    else:
                        await self.client.say("<@{}> found {}".format(eggcheck.author.id, eggfindings[didwin]))
                        await self.client.delete_message(eggcheck)
            await self.client.say("Now you'll have to wait another 5 minutes to use the d!minigame command")
        elif picked == minigame[1]:
            await self.client.say("Minigame started: Type 'Search *number*' untill you find the 💎 (Number between 1-100)")
            searchednumber = random.randint(1,100)
            print(searchednumber)
            diafound = False
            while diafound == False:
                diasearch = await self.client.wait_for_message()
                if diasearch.content.upper() == "SEARCH {}".format(searchednumber):
                    await self.client.say("<@{}> just found the 💎".format(diasearch.author.id))
                    await self.client.delete_message(diafound)
                    diafound = True
                elif diasearch.content.upper().startswith("SEARCH"):
                    await self.client.say("<@{}> found nothing, keep searching!".format(diasearch.author.id))
                    await self.client.delete_message(diafound)
            await self.client.say("Now you'll have to wait another 5 minutes to use the d!minigame command")

    @commands.command(pass_context=True)
    async def joinc(self, ctx, channel: discord.Channel):
        if checks.dragonmaster(ctx.message.server, ctx.message.author):
            sql.SetWelcomeChannel(ctx.message.server.id, channel.id)
            await self.client.say("`{}` **is now set as the welcome channel**".format(channel.name))

    @commands.command(pass_context=True)
    async def creds(self, ctx):
        SponsorTitle = "Credits"
        SponsorMessage = "**Dragon's Developers**\n**Main Developer:** Flop#1536\n**Software Engineer:** Z4mbi3#6399\n**Other inputs from the community / Ilysi's Development Team.**"
        em = dmbd.infopage(SponsorTitle, SponsorMessage)
        await self.client.delete_message(ctx.message)
        await self.client.say(embed=em)

    @commands.command(pass_context=True)
    async def invite(self, ctx):
        SponsorTitle = "Invite"
        SponsorMessage = "**Want to get Dragon on your own server ?**\n[Invite me here](https://discordapp.com/oauth2/authorize?client_id=402246509313392640&permissions=942927063&scope=bot)"
        em = dmbd.infopage(SponsorTitle, SponsorMessage)
        await self.client.delete_message(ctx.message)
        await self.client.say(embed=em)

    @commands.command(pass_context=True)
    async def translate(self, ctx, language: str, *, content: str):
        title = "Translate"
        translation = translate(content, language)
        content = content + "\n**Translates to**\n" + translation + "\n**in " + language + "**"
        em = dmbd.infopage(title, content)
        await self.client.say(embed=em)
        await self.client.delete_message(ctx.message)


def setup(client):
    client.add_cog(Basic(client))
