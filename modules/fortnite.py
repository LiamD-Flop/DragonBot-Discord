import discord
from discord.ext import commands
import pynite
import asyncio
import tools.discordembed as dmbd

fortnite = pynite.Client('faaa3d3a-209c-46d6-9cf0-8ee59232e226', timeout=5)
client = commands.Bot(command_prefix = "d!")

def cleanprinting(k):
    basi = str(k)
    basi = basi.strip("\{\}")
    basi = basi.split(",")
    y = 0
    while y < len(basi):
        print(y)
        if "'displayValue':" in basi[y]:
            clean = basi[y]
            clean = clean.strip("'displayValue': ")
            break
        else:
            y += 1
    return clean
class Fortnite:

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def fnsolo(self, ctx, *, content: str):
        '''Fetch a profile.'''
        content = content.split()
        print(content)
        platform = content[1]
        name = content[0]
        player = await fortnite.get_player(platform, name)
        solos = await player.get_solos()
        skills = solos.kills
        pt = cleanprinting(solos.minutes_played)
        kills = "\n**Kills:** " + cleanprinting(solos.kills) + "\n**K/D:** {}".format(cleanprinting(solos.kd)) + "\n**KPG:** " + cleanprinting(solos.kpg)
        matches = "\n**Matches:** " + cleanprinting(solos.matches) + "\n**Score/Match:** " + cleanprinting(solos.score_per_match)
        em = dmbd.fortniteemb(n=name, st="Solo", pt=pt, kd=kills, m=matches, pf=platform)
        await self.client.say(embed=em)

    @commands.command(pass_context=True)
    async def fnduo(self, ctx, *, content: str):
        '''Fetch a profile.'''
        content = content.split()
        print(content)
        platform = content[1]
        name = content[0]
        player = await fortnite.get_player(platform, name)
        solos = await player.get_duos()
        skills = solos.kills
        pt = cleanprinting(solos.minutes_played)
        kills = "\n**Kills:** " + cleanprinting(solos.kills) + "\n**K/D:** {}".format(cleanprinting(solos.kd)) + "\n**KPG:** " + cleanprinting(solos.kpg)
        matches = "\n**Matches:** " + cleanprinting(solos.matches) + "\n**Score/Match:** " + cleanprinting(solos.score_per_match)
        em = dmbd.fortniteemb(n=name, st="Duo", pt=pt, kd=kills, m=matches, pf=platform)
        await self.client.say(embed=em)

    @commands.command(pass_context=True)
    async def fnsquad(self, ctx, *, content: str):
        '''Fetch a profile.'''
        content = content.split()
        print(content)
        platform = content[1]
        name = content[0]
        player = await fortnite.get_player(platform, name)
        solos = await player.get_squads()
        skills = solos.kills
        pt = cleanprinting(solos.minutes_played)
        kills = "\n**Kills:** " + cleanprinting(solos.kills) + "\n**K/D:** {}".format(cleanprinting(solos.kd)) + "\n**KPG:** " + cleanprinting(solos.kpg)
        matches = "\n**Matches:** " + cleanprinting(solos.matches) + "\n**Score/Match:** " + cleanprinting(solos.score_per_match)
        em = dmbd.fortniteemb(n=name, st="Squad", pt=pt, kd=kills, m=matches, pf=platform)
        await self.client.say(embed=em)

def setup(client):
    client.add_cog(Fortnite(client))
