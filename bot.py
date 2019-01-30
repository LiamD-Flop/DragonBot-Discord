import asyncio
import time
import random
import discord
import os
import ast
from discord.ext import commands
from discord.ext.commands import Bot
import tools.checks as checks
from time import strftime
import tools.discordembed as dmbd
import tools.colorprint as clrp
import tools.dragonsql as sql
import tools.serversql as ssql
import tools.ImageTools as imgt
import aiohttp
from itertools import cycle

def CheckInName(n):
    if "'" in n:
        msg = ""
        for y in n:
            if y == "'":
                msg = msg+y+"'"
            else:
                msg = msg+y
    else:
        msg = n
    return msg


Client = discord.Client()
client = commands.Bot(command_prefix=commands.when_mentioned_or("d!"))
client.remove_command('help')
Purgemax = 31
dbltoken = ""
url = ""
headers = {"Authorization" : dbltoken}

check = {
    'modules.fun',
    'modules.musicplayer',
    'modules.rainbowsix',
    'modules.basic',
    'modules.bank',
    'modules.crew',
    'modules.support',
    'modules.developer'
}

random.seed()
try:
    for x in check:
        client.load_extension(x)
except ImportError as e:
    print(e)
    print(clrp.ERROR+'[WARNING] : One or more modules did not import.'+clrp.RESET)

async def change_status():
    await client.wait_until_ready()
    serveram = len(client.servers)
    game = "{} Servers | d!info".format(str(serveram))
    msg = cycle([game, "Flop struggle on my reworked version"])

    while not client.is_closed:
        current_stat = next(msg)
        await client.change_presence(game=discord.Game(name=current_stat, type=3))
        await asyncio.sleep(30)


@client.event
async def on_server_join(server):
    if not "dragon master" in [y.name.lower() for y in server.roles]:
        serveram = len(client.servers)
        game = "{} Servers | d!info".format(str(serveram))
        await client.change_presence(game=discord.Game(name=game, url="https://liamd.pw/", type=3))
        await client.create_role(server, name="Dragon Master", permisssions=70503488)
        await client.send_message(server.owner, "Make sure to add yourself to *Dragon Master*, then you are able to use the Moderation Commands")
    payload = {"server_count"  : len(client.servers)}
    async with aiohttp.ClientSession() as aioclient:
            await aioclient.post(url, data=payload, headers=headers)
    if not ssql.InServer(server.id):
        ssql.NewServer(server.id, server.owner.id, CheckInName(server.name))


@client.event
async def on_ready():
    os.system('clear')
    pid = os.getpid()
    activecheck = open("/home/dbot/DragonTesting/activecheck.txt", "w")
    activecheck.write(str(pid))
    activecheck.close()
    print(clrp.STARTUP+'Dragon is up and running.'+clrp.RESET)
    serveram = len(client.servers)
    game = "{} Servers | d!info".format(str(serveram))
    await client.change_presence(game=discord.Game(name=game, url="http://dragon.ilysi.com/", type=3))
    payload = {"server_count"  : len(client.servers)}
    async with aiohttp.ClientSession() as aioclient:
            await aioclient.post(url, data=payload, headers=headers)

@client.event
async def on_member_join(member):
    if sql.WelcomeChannelSet(member.server.id):
        avatar = "https://cdn.discordapp.com/avatars/{}/{}.png".format(member.id, member.avatar)
        img = imgt.ImageWrite(imgurl=avatar, name="{}#{}".format(member.name, member.discriminator), server=member.server.name)
        await client.send_file(member.server.get_channel(str(sql.GetWelcomeChannel(member.server.id))), img[0])
        for y in img:
            os.remove(y)

@client.event
async def on_message(message):
    if not message.author.bot:
        commandtest = message.content.split("!")
        if not message.channel.is_private:
            if commandtest[0] == "d" or message.content.startswith("<@402246509313392640>"):
                    if sql.CheckBan(message.author.id):
                        Banmessage = "Sorry {}, you are banned from using Dragon. Want an unban ? Send a message to Flop#1536.".format(message.author.mention)
                        await client.send_message(message.author, Banmessage)
                        print(clrp.WARNING+"{} is banned and used the command: {}".format(message.author.name, message.content)+clrp.RESET)
                        await client.delete_message(message)
                    elif message.content.startswith("<@"):
                        if client.get_command(message.content.split()[1]):
                            await client.process_commands(message)
                            print(clrp.LOG+"{} used the command: {}".format(message.author.id, message.content)+clrp.RESET)
                        else:
                            #sendmessage = "I do not know the command **" + commandtest[1] + "**. Please check for typos " + message.author.name
                            await client.delete_message(message)
                            #await client.send_message(message.channel, sendmessage)
                    elif client.get_command(commandtest[1]):
                        await client.process_commands(message)
                        print(clrp.LOG+"{} used the command: {}".format(message.author.id, message.content)+clrp.RESET)
                    else:
                        #sendmessage = "I do not know the command **" + commandtest[1] + "**. Please check for typos " + message.author.name
                        await client.delete_message(message)
                        #await client.send_message(message.channel, sendmessage)


@client.event
async def on_server_remove(server):
    payload = {"server_count"  : len(client.servers)}
    async with aiohttp.ClientSession() as aioclient:
            await aioclient.post(url, data=payload, headers=headers)

@client.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        seconds = error.retry_after
        minutes = int(error.retry_after // 60)
        seconds = int(seconds - (minutes*60))
        if ctx.message.content.startswith('d!crime'):
            em = dmbd.econembed('You can commit a crime in {}m {}s'.format(minutes, seconds))
            await client.send_message(ctx.message.channel, embed=em)
        elif ctx.message.content.startswith('d!work'):
            em = dmbd.econembed('You can work in {}m {}s'.format(minutes, seconds))
            await client.send_message(ctx.message.channel, embed=em)
        elif ctx.message.content.startswith('d!pimp'):
            em = dmbd.econembed('You can pimp in {}m {}s'.format(minutes, seconds))
            await client.send_message(ctx.message.channel, embed=em)
        elif ctx.message.content.startswith('d!mug'):
            em = dmbd.econembed('You can mug someone in {}m {}s'.format(minutes, seconds))
            await client.send_message(ctx.message.channel, embed=em)
        elif ctx.message.content.startswith('d!heist'):
            em = dmbd.econembed('You can start another heist in {}m {}s'.format(minutes, seconds))
            await client.send_message(ctx.message.channel, embed=em)
        elif ctx.message.content.startswith('d!bankhack'):
            em = dmbd.econembed('You can start hacking in {}m {}s'.format(minutes, seconds))
            await client.send_message(ctx.message.channel, embed=em)
    else:
        print(clrp.ERROR+"==========An Error Occured=========="+clrp.RESET)
        raise error

client.loop.create_task(change_status())
client.run("")
