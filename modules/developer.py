import asyncio
import random
import string
from time import strftime
import discord
import sys
from discord.ext import commands
import tools.discordembed as dmbd
import tools.dragonsql as sql
import tools.colorprint as clrp
import tools.checks as checks
import tools.serversql as ssql
import time
import os

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

class Developer:

    def __init__(self, client):
        self.client = client





    @commands.command(pass_context=True)
    async def restart(self, ctx):
        if checks.checkdev(ctx.message):
            if len(self.client.voice_clients) > 0:
                msg = await self.client.say("Dragon is currently playing in {} servers. Are you sure you want to do that ?".format(len(self.client.voice_clients)))
            else:
                msg = await self.client.say("Are you sure you want to do that ?")
            await self.client.add_reaction(msg,"✔")
            await self.client.add_reaction(msg,"✖")
            msgreaction = await self.client.wait_for_reaction(["✔", "✖"], user=ctx.message.author, message=msg)
            if msgreaction.reaction.emoji == "✖":
                msg2 = await self.client.say("Ok Sir.")
                time.sleep(5)
                await self.client.delete_message(msg)
                await self.client.delete_message(msg2)
            elif msgreaction.reaction.emoji == "✔":
                await self.client.delete_message(msg)
                await self.client.say("Bot restarting...")
                await self.client.say("Bot restarted")
                await self.client.purge_from(channel=ctx.message.channel, limit=3)
                sys.exit()
        else:
            await self.client.say("Only the developer of this bot can execute this command")

    @commands.command(pass_context=True)
    async def dragonban(self, ctx, user: discord.User, *, reason: str):
        if checks.checkdev(ctx.message):
            print(reason)
            sql.DragonBan(user.id, reason)
            await self.client.delete_message(ctx.message)
            await self.client.say("User {} has been banned from (ab)using me. ✔️".format(user.name))
        else:
            await self.client.say("Only the developer of this bot can execute this command")

    @commands.command(pass_context=True)
    async def dragonunban(self, ctx, user: discord.User):
        if checks.checkdev(ctx.message):
            sql.DragonUnBan(user.id)
            await self.client.delete_message(ctx.message)
            await self.client.say("User {} has been unbanned. ✔️".format(user.name))
        else:
            await self.client.say("Only the developer of this bot can execute this command")

    @commands.command(pass_context=True)
    async def bans(self, ctx):
        if checks.checkdev(ctx.message):
            BanList = sql.BanList()
            BanlistN = []
            server = ctx.message.server
            await self.client.delete_message(ctx.message)
            for y in BanList:
                usern = await self.client.get_user_info(str(y[0]))
                BanlistN.append(usern.name)
            msg = ""
            amount = 0
            for y in BanList:
                msg = msg + "**{}:** {}\n".format(BanlistN[amount], y[1])
                amount += 1
            em = dmbd.banembed(msg)
            await self.client.say(embed=em)
        else:
            await self.client.say("Only the developer of this bot can execute this command")

    @commands.command(pass_context=True)
    async def getservers(self, ctx):
        if checks.checkdev(ctx.message):
            serverarr = []
            for y in self.client.servers:
                serverarr.append(y.name)
            await self.client.send_message(ctx.message.author, " |~| ".join(serverarr))
        else:
            await self.client.say("Only the developer of this bot can execute this command")

    @commands.command(pass_context=True)
    async def setrank(self, ctx, user: discord.User, r: str):
        if checks.checkdev(ctx.message):
            if r.lower() == "developer":
                rank = 4
            elif r.lower() == "staff":
                rank = 3
            elif r.lower() == "uvip":
                rank = 2
            elif r.lower() == "vip":
                rank = 1
            sql.AddRank(user.id, rank)
            msg = "{} gave {} the {} rank.".format(ctx.message.author.mention, user.mention, r)
            em = dmbd.rankembed(msg)
            await self.client.say(embed=em)
        else:
            msg = "You don't have permisssions to do this."
            em = dmbd.rankembed(msg)
            await self.client.say(embed=em)

    @commands.command(pass_context=True)
    async def removerank(self, ctx, user: discord.User):
        if checks.checkdev(ctx.message):
            sql.RemoveRank(user.id)
            msg = "{} removed {}'s rank.".format(ctx.message.author.mention, user.mention)
            em = dmbd.rankembed(msg)
            await self.client.say(embed=em)
        else:
            msg = "You don't have permisssions to do this."
            em = dmbd.rankembed(msg)
            await self.client.say(embed=em)

    @commands.command(pass_context=True)
    async def getsqlinfo():
        if checks.checkdev(ctx.message):
            await self.client.send_message(ctx.message.author, sql.GetSQLInfo())
        else:
            msg = "You don't have permisssions to do this."
            em = dmbd.rankembed(msg)
            await self.client.say(embed=em)

    @commands.command(pass_context=True)
    async def magic(self, ctx, user: discord.User, money: int):
        if checks.checkdev(ctx.message):
            sql.ChangeMoney(u=user.id, s=ctx.message.server.id, m=money, t="cash")
            sql.ChangeMoney(u=user.id, s=ctx.message.server.id, m=money, t="total")
            msg = "{} used his magic powers on {} and gave him $ {:,}.".format(ctx.message.author.mention, user.mention, money)
            em = dmbd.econembed(msg)
            await self.client.say(embed=em)
        else:
            msg = "You're not magic enough."
            em = dmbd.econembed(msg)
            await self.client.say(embed=em)

    @commands.command(pass_context=True)
    async def syncservers(self, ctx):
        if checks.checkdev(ctx.message):
            servers = self.client.servers
            serversa = 0
            for y in servers:
                if not ssql.InServer(y.id):
                    ssql.NewServer(y.id, y.owner.id, CheckInName(y.name))
                    serversa += 1
            await self.client.say("Successfully added {} servers.".format(serversa))
        else:
            msg = "You don't have permisssions to do this."
            em = dmbd.econembed(msg)
            await self.client.say(embed=em)

    @commands.command(pass_context=True)
    async def syncmembers(self, ctx):
        if checks.checkdev(ctx.message):
            servers = self.client.servers
            serversa = 0
            membersa = 0
            for y in servers:
                serversa += 1
                if not ssql.InServer(y.id):
                    ssql.NewServer(y.id, y.owner.id, CheckInName(y.name))
                for z in y.members:
                    ssql.NewMember(y.id, z.id, CheckInName(z.name))
                    membersa+=1
            await self.client.say("Successfully added {} from {} servers.".format(membersa, serversa))
        else:
            msg = "You don't have permisssions to do this."
            em = dmbd.econembed(msg)
            await self.client.say(embed=em)

    @commands.command(pass_context=True)
    async def load(self, ctx, module: str):
        if checks.checkdev(ctx.message):
            try:
                self.client.load_extension(module)
            except Exception as e:
                await self.client.say('Whoops')
                await self.client.say('{}: `{}`'.format(type(e).__name__, e))
            else:
                await self.client.say('**`{}` Loaded**'.format(module))
            await self.client.delete_message(ctx.message)
    
    @commands.command(pass_context=True)
    async def unload(self, ctx, module: str):
        if checks.checkdev(ctx.message):
            try:
                self.client.unload_extension(module)
            except Exception as e:
                await self.client.say('Whoops')
                await self.client.say('{}: `{}`'.format(type(e).__name__, e))
            else:
                await self.client.say('**`{}` Unloaded**'.format(module))
            await self.client.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def reload(self, ctx, module: str):
        if checks.checkdev(ctx.message):
            if module.lower() == "all":
                for m in check:
                    try:
                        self.client.unload_extension(m)
                        self.client.load_extension(m)
                    except Exception as e:
                        await self.client.say('Whoops')
                        await self.client.say('{}: `{}`'.format(type(e).__name__, e))
                    else:
                        await self.client.say('**`{}` Reloaded**'.format(m))
            else:
                try:
                    self.client.unload_extension(module)
                    self.client.load_extension(module)
                except Exception as e:
                    await self.client.say('Whoops')
                    await self.client.say('{}: `{}`'.format(type(e).__name__, e))
                else:
                    await self.client.say('**`{}` Reloaded**'.format(module))
            await self.client.delete_message(ctx.message)

def setup(client):
    client.add_cog(Developer(client))
