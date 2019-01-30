import asyncio
import discord
import tools.colorprint as clrp
import os

from discord.ext import commands
from discord.ext.commands import Bot

Client = discord.Client()
client = commands.Bot(command_prefix=commands.when_mentioned_or("d!"))

class Startup:

    def __init__(self, client):
        self.client = client

    @client.event
    async def on_ready():
        os.system('clear')
        pid = os.getpid()
        activecheck = open("/home/dbot/DragonTesting/activecheck.txt", "w")
        activecheck.write(str(pid))
        activecheck.close()
        print(clrp.STARTUP+'Dragon is up and running.'+clrp.RESET)
        serveram = len(self.client.servers)
        game = "{} Servers | dt!info".format(str(serveram))
        await self.client.change_presence(game=discord.Game(name=game, url="http://dragon.ilysi.com/", type=3))
        payload = {"server_count"  : len(self.client.servers)}
        async with aiohttp.ClientSession() as aioclient:
            await aioclient.post(url, data=payload, headers=headers)

def setup(client):
    client.add_cog(Startup(client))
