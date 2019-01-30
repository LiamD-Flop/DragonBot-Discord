import discord
from discord.ext import commands
import tools.discordembed as dmbd


class RainbowSix:

    def __init__(self, client):
        self.client = client


    @commands.command(pass_context=True)
    async def r6stats(self, ctx, *, content: str):
        content = content.split()
        if content[1].lower() == "uplay" or content[1].lower() == "pc" or content[1] == None:
            platform = api.Platforms.UPLAY
        elif content[1].lower() == "xbox" or content[1].lower() == "360":
            platform = api.Platforms.XBOX
        elif content[1].lower() == "playstation" or content[1].lower() == "ps4" :
            platform = api.Platforms.PLAYSTATION
        player = await auth.get_player(content[0], platform)
        await player.load_general()
        headshots = player.headshots
        time = player.time_played
        hours = time // 3600
        time %= 3600
        minutes = time // 60
        pt = '{} hours and {} minutes'.format(hours, minutes)
        if player.deaths == 0:
            kills = "**Kills:** " + str(player.kills) + "\n**Deaths:** " + str(player.deaths) + "**K/D:** {0:.2f}".format((player.kills))
        else:
            kills = "**Kills:** " + str(player.kills) + "\n**Deaths:** " + str(player.deaths) + "**K/D:** {0:.2f}".format((player.kills / player.deaths))
        if player.bullets_fired == 0:
            shot = "**Shots Fired:** " + str(player.bullets_fired) + "\n**Shots Hit:** " + str(player.bullets_hit) + "\n**Accuracy:** {0:.2f}%".format((player.bullets_hit))
        else:
            shot = "**Shots Fired:** " + str(player.bullets_fired) + "\n**Shots Hit:** " + str(player.bullets_hit) + "\n**Accuracy:** {0:.2f}%".format((player.bullets_hit / player.bullets_fired * 100))
        match = "**Matches Player:** " + str(player.matches_played) + "\n**Matches Won:** " + str(player.matches_won) + "\n**Matches Lost:** " + str(player.matches_lost)
        spec = "**Revives:** " + str(player.revives) + "\n**Melee Kills:** " + str(player.melee_kills)
        await player.load_level()
        xp = "**XP:** " + str(player.xp) + "\n**Level:** " + str(player.level)
        em = dmbd.rainbowgeneral(n=content[0], pt=pt, k=kills, s=shot, m=match, x=xp, sp=spec)
        await self.client.say(embed=em)

    @commands.command(pass_context=True)
    async def r6rank(self, ctx, *, content: str):
        content = content.split()
        if content[1].lower() == "uplay" or content[1].lower() == "pc" or content[1] == None:
            platform = api.Platforms.UPLAY
        elif content[1].lower() == "xbox" or content[1].lower() == "360":
            platform = api.Platforms.XBOX
        elif content[1].lower() == "playstation" or content[1].lower() == "ps4" :
            platform = api.Platforms.PLAYSTATION
        player = await auth.get_player(content[0], platform)
        await player.load_rank("EU")
        await self.client.say(player.mmr)

def setup(client):
    client.add_cog(RainbowSix(client))
