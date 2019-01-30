import asyncio
import discord
import tools.colorprint as clrp
import os

from discord.ext import commands
from discord.ext.commands import Bot

Client = discord.Client()
client = commands.Bot(command_prefix=commands.when_mentioned_or("d!"))

class Sessionhandler:

    def __init__(self, client):
        self.client = client

    @client.event
    async def on_server_join(server):
        if not "dragon master" in [y.name.lower() for y in server.roles]:
            serveram = len(self.client.servers)
            game = "{} Servers | dt!info".format(str(serveram))
            await self.client.change_presence(game=discord.Game(name=game, url="https://liamd.pw/", type=3))
            await self.client.create_role(server, name="Dragon Master", permisssions=70503488)
            await self.client.send_message(server.owner, "Make sure to add yourself to *Dragon Master*, then you are able to use the Moderation Commands")
        payload = {"server_count"  : len(self.client.servers)}
        async with aiohttp.ClientSession() as aioclient:
                await aioclient.post(url, data=payload, headers=headers)
        if not ssql.InServer(server.id):
            ssql.NewServer(server.id, server.owner.id, CheckInName(server.name))


    @client.event
    async def on_server_remove(server):
        payload = {"server_count"  : len(self.client.servers)}
        async with aiohttp.ClientSession() as aioclient:
                await aioclient.post(url, data=payload, headers=headers)


def setup(client):
    client.add_cog(Sessionhandler(client))
