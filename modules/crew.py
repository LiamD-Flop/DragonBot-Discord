import asyncio
import random
import string
from time import strftime
import discord
from discord.ext import commands
import tools.discordembed as dmbd
import tools.dragonsql as sql
import tools.colorprint as clrp
import tools.checks as checks
import time

class Crew:

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def createcrew(self, ctx, *, name: str):
        if not sql.CheckUserExist(u=ctx.message.author.id, s=ctx.message.server.id):
            sql.NewBankUser(u=ctx.message.author.id, s=ctx.message.server.id)
        balance = sql.GetBalance(u=ctx.message.author.id, s=ctx.message.server.id)
        if balance[1] >= 10000000:
            sql.ChangeMoney(u=ctx.message.author.id, s=ctx.message.server.id, m=-10000000, t="bank")
            sql.CreateCrew(u=ctx.message.author.id, s=ctx.message.server.id, n=name)
            msg = "You created the crew {}.".format(name)
            em = dmbd.crewembed(msg)
            await self.client.say(embed=em)
        else:
            msg = "You need $ 10,000,000 in your bank to start a crew.".format(name)
            em = dmbd.crewembed(msg)
            await self.client.say(embed=em)

    @commands.command(pass_context=True)
    async def crewinvite(self, ctx, user: discord.User):
        if sql.CheckCOwner(u=ctx.message.author.id, s=ctx.message.server.id):
            if not sql.CheckUserInCrew(user.id):
                crew = sql.GetCrew(u=ctx.message.author.id)
                crewi = crew[0]
                msg = "{} invited {} to {}.".format(ctx.message.author.name, user.mention, crew[1])
                em = dmbd.crewembed(msg)
                invitemsg = await self.client.say(embed=em)
                await self.client.add_reaction(invitemsg, "✔")
                await self.client.add_reaction(invitemsg, "✖")
                time.sleep(1)
                CheckReact = await self.client.wait_for_reaction(["✔", "✖"], user=user, message=invitemsg)
                if str(CheckReact.reaction.emoji) ==  "✔":
                    sql.JoinCrew(c=crewi, u=user.id)
                    msg = "User joined the crew."
                    em = dmbd.crewembed(msg)
                    await self.client.say(embed=em)
                elif str(CheckReact.reaction.emoji) ==  "✖":
                    await self.client.delete_message(invitemsg)
            else:
                msg = "User already in a crew."
                em = dmbd.crewembed(msg)
                await self.client.say(embed=em)
        else:
            msg = "You don't own a crew.".format(ctx.message.author.name)
            em = dmbd.crewembed(msg)
            await self.client.say(embed=em)

    @commands.command(pass_context=True)
    async def vaultdep(self, ctx, money: int):
        money = abs(money)
        if sql.CheckUserInCrew(ctx.message.author.id):
            crew = sql.GetMemCrew(u=ctx.message.author.id, s=ctx.message.server.id)
            cash = sql.GetBalance(u=ctx.message.author.id, s=ctx.message.server.id)[1]
            if money <= cash:
                sql.ChangeMoney(u=ctx.message.author.id, s=ctx.message.server.id, m=-money, t="bank")
                sql.ChangeCrewVault(u=ctx.message.author.id, c=crew[0], m=money)
                msg = "You deposited $ {:,} into your crew vault.".format(money)
                em = dmbd.crewembed(msg)
                await self.client.say(embed=em)
            else:
                msg = "You don't have $ {:,}.".format(money)
                em = dmbd.crewembed(msg)
                await self.client.say(embed=em)

    @commands.command(pass_context=True)
    async def crewinfo(self, ctx, user: discord.User = None):
        if user == None:
            if sql.CheckUserInCrew(ctx.message.author.id):
                crews = sql.GetMemCrew(u=ctx.message.author.id, s=ctx.message.server.id)
                crew = sql.GetCrewInfo(c=crews[0])
                memberids = []
                for y in crew:
                    memberids.append(y[0])
                print(memberids)
                members = len(crew)
                vault = (crew[0])[3]
                owner = (crew[0])[2]
                owner = (await self.client.get_user_info(str(owner))).name
                name = (crew[0])[1]
                msg = "**{}**\n**Members:** {}\n**Owner:** {}\n**Vault:** $ xxx,xxx,xxx.".format(name, members, owner)
                em = dmbd.crewembed(msg)
                themsg = await self.client.say(embed=em)
                await self.client.add_reaction(themsg, "💰")
                Reaction = await self.client.wait_for_reaction("💰", message=themsg, user=ctx.message.author, timeout=60)
                if Reaction and not Reaction.user.id == self.client.user.id:
                    RUser = sql.GetMemCrew(u=Reaction.user.id, s=ctx.message.server.id)
                    if RUser[0] == crews[0]:
                        user = (await self.client.get_user_info(str(RUser[1])))
                        await self.client.send_message(user, "Your crew vault: $ {:,}".format(vault))
        else:
            if sql.CheckUserInCrew(user.id):
                crews = sql.GetMemCrew(u=user.id, s=ctx.message.server.id)
                crew = sql.GetCrewInfo(c=crews[0])
                memberids = []
                for y in crew:
                    memberids.append(y[0])
                members = len(crew)
                vault = (crew[0])[3]
                owner = (crew[0])[2]
                owner = (await self.client.get_user_info(str(owner))).name
                name = (crew[0])[1]
                msg = "**{}**\n**Members:** {}\n**Founder:** {}\n**Vault:** $ xxx,xxx,xxx.".format(name, members, owner)
                em = dmbd.crewembed(msg)
                themsg = await self.client.say(embed=em)
                await self.client.add_reaction(themsg, "💰")
                Reaction = await self.client.wait_for_reaction("💰", message=themsg, user=user, timeout=60)
                if Reaction and not Reaction.user.id == self.client.user.id:
                    RUser = sql.GetMemCrew(u=Reaction.user.id, s=ctx.message.server.id)
                    if RUser[0] == crews[0]:
                        user = (await self.client.get_user_info(str(RUser[1])))
                        await self.client.send_message(user, "Your crew vault: $ {:,}".format(vault))




def setup(client):
    client.add_cog(Crew(client))
