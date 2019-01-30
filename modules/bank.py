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

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def Booster(u):
    rank = sql.CheckBoosters(u)
    if rank == 4 or rank == 2:
        booster = 0.1
    elif rank == 1:
        booster = 0.05
    elif rank == 0 or rank == 3:
        booster = 0
    return booster

def MoneyBoost(u):
    rank = sql.CheckBoosters(u)
    if rank == 4 or rank == 2:
        booster = 1.2
    elif rank == 1:
        booster = 1.1
    elif rank == 0 or rank == 3:
        booster = 1
    return booster

def SetSlots(n):
    if n == 1:
        return ":one:"
    elif n == 2:
        return ":two:"
    elif n == 3:
        return ":three:"
    elif n == 4:
        return ":four:"
    elif n == 5:
        return ":five:"
    elif n == 6:
        return ":six:"
    elif n == 7:
        return ":seven:"
    elif n == 8:
        return ":eight:"
    elif n == 9:
        return ":nine:"



class Bank:

    def __init__(self, client):
        self.client = client


    @commands.command(pass_context=True)
    async def balcreate(self, ctx):
        newuser = sql.NewBankUser(u=ctx.message.author.id, s=ctx.message.server.id)
        if newuser:
            em = dmbd.econembed("Your account has been created.")
        else:
            em = dmbd.econembed("You already own an account on this server.")
        await self.client.say(embed=em)

    @commands.command(pass_context=True)
    async def bal(self, ctx):
        if not sql.CheckUserExist(u=ctx.message.author.id, s=ctx.message.server.id):
            sql.NewBankUser(u=ctx.message.author.id, s=ctx.message.server.id)
        newuser = sql.GetBalance(u=ctx.message.author.id, s=ctx.message.server.id)
        cash = newuser[0]
        bank = newuser[1]
        total = newuser[2]
        msg = "**Cash:** $ {:,}\n\n**Bank:** $ {:,}\n\n**Total Earnings:** $ {:,}".format(cash, bank, total)
        em = dmbd.econembed(msg)
        await self.client.say(embed=em)

    @commands.command(pass_context=True)
    async def leaderboard(self, ctx):
        server = ctx.message.server
        LeaderB = sql.BankLeaderboard(s=server.id)
        totallist = len(LeaderB)
        total = sum(int(i[1]) for i in LeaderB)
        e = 0
        tmsg = "**Server Total:** $ {:,}\n".format(total)
        while e < 5 and e <= totallist:
            first = LeaderB[e]
            id = str(first[0])
            id = await self.client.get_user_info(id)
            firstn = id.name
            e+=1
            tmsg = tmsg + "\n**{}) {}:** $ {:,}".format(e, firstn, first[1])
        msg = tmsg
        em = dmbd.econembed(msg)
        await self.client.say(embed=em)

    @commands.command(pass_context=True)
    async def deposit(self, ctx, money: int):
        money = abs(money)
        if not sql.CheckUserExist(u=ctx.message.author.id, s=ctx.message.server.id):
            sql.NewBankUser(u=ctx.message.author.id, s=ctx.message.server.id)
        cash = sql.GetBalance(u=ctx.message.author.id, s=ctx.message.server.id)[0]
        if money <= cash:
            sql.ChangeMoney(u=ctx.message.author.id, s=ctx.message.server.id, m=money, t="bank")
            sql.ChangeMoney(u=ctx.message.author.id, s=ctx.message.server.id, m=-money, t="cash")
            msg = "**You deposited `$ {:,}` into your bank account.**".format(money)
            await self.client.say(msg)
        else:
            msg = "**You don't have `$ {:,}`.**".format(money)
            await self.client.say(msg)

    @commands.command(pass_context=True)
    async def withdraw(self, ctx, money: int):
        money = abs(money)
        if not sql.CheckUserExist(u=ctx.message.author.id, s=ctx.message.server.id):
            sql.NewBankUser(u=ctx.message.author.id, s=ctx.message.server.id)
        bank = sql.GetBalance(u=ctx.message.author.id, s=ctx.message.server.id)[1]
        if money <= bank:
            sql.ChangeMoney(u=ctx.message.author.id, s=ctx.message.server.id, m=money, t="cash")
            sql.ChangeMoney(u=ctx.message.author.id, s=ctx.message.server.id, m=-money, t="bank")
            msg = "**You withdrew `$ {:,}`.**".format(money)
            await self.client.say(msg)
        else:
            msg = "**You don't have `$ {:,}`.**".format(money)
            await self.client.say(msg)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def crime(self, ctx):
        if not sql.CheckUserExist(u=ctx.message.author.id, s=ctx.message.server.id):
            sql.NewBankUser(u=ctx.message.author.id, s=ctx.message.server.id)
        rand = random.randint(0,10)
        chance = random.randint(0,10)
        money = int(random.randint(400,482000) * MoneyBoost(ctx.message.author.id))
        if rand < chance:
            sql.ChangeMoney(u=ctx.message.author.id, s=ctx.message.server.id, m=money,t="cash")
            sql.ChangeMoney(u=ctx.message.author.id, s=ctx.message.server.id, m=money,t="total")
            msg = "**You stole `$ {:,}`.**".format(money)
            await self.client.say(msg)
        else:
            mone = -(money/2)
            sql.ChangeMoney(u=ctx.message.author.id, s=ctx.message.server.id, m=mone,t="bank")
            msg = "**You failed the crime and payed a `$ {:,}`** fine.".format(money/2)
            await self.client.say(msg)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def work(self, ctx):
        if not sql.CheckUserExist(u=ctx.message.author.id, s=ctx.message.server.id):
            sql.NewBankUser(u=ctx.message.author.id, s=ctx.message.server.id)
        money = int(random.randint(400,8000) * MoneyBoost(ctx.message.author.id))
        sql.ChangeMoney(u=ctx.message.author.id, s=ctx.message.server.id, m=money,t="bank")
        sql.ChangeMoney(u=ctx.message.author.id, s=ctx.message.server.id, m=money,t="total")
        msg = "**You received a paycheck of `$ {:,}`.**".format(money)
        await self.client.say(msg)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 900, commands.BucketType.user)
    async def mug(self, ctx, user: discord.User):
        if not sql.CheckUserExist(u=ctx.message.author.id, s=ctx.message.server.id):
            sql.NewBankUser(u=ctx.message.author.id, s=ctx.message.server.id)
        if not (user == ctx.message.author):
            cash = sql.Mug(u=user.id, s=ctx.message.server.id)
            if cash > 0:
                sql.ChangeMoney(u=ctx.message.author.id, s=ctx.message.server.id, m=cash, t="cash")
                sql.ChangeMoney(u=ctx.message.author.id, s=ctx.message.server.id, m=cash, t="total")
                msg = "**You mugged `{}` and took `$ {:,}`.**".format(user.name, cash)
                em = dmbd.econembed(msg)
                await self.client.say(embed=em)
            else:
                msg = "`{}` **hasn't got any money on them.**".format(user.name)
                await self.client.say(msg)
        else:
            msg = "You can't mug yourself."
            em = dmbd.econembed(msg)
            await self.client.say(embed=em)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 900, commands.BucketType.server)
    async def heist(self, ctx):
        if not sql.CheckUserExist(u=ctx.message.author.id, s=ctx.message.server.id):
            sql.NewBankUser(u=ctx.message.author.id, s=ctx.message.server.id)
        HeistPrep = True
        HeistPot = int(random.randint(200000,2000000) * MoneyBoost(ctx.message.author.id))
        HeistMemID = [ctx.message.author.id]
        HeistMemName = [ctx.message.author.name]
        HeistCount = 1
        HeistChance = 0.11 + Booster(ctx.message.author.id)
        msg = "**Heist**\n\n**Joined Players:** \n{}\n{}/4\n\n**HeistChance:** {}%\n\n**Heist Payout:** $ {:,}\n\n**Join Now:** 🌐".format(" ".join(HeistMemName), HeistCount, int(HeistChance*100), HeistPot)
        em = dmbd.econembed(msg)
        HeistAnnounce = await self.client.say(embed=em)
        await self.client.add_reaction(HeistAnnounce, "🌐")
        time.sleep(1)
        await self.client.add_reaction(HeistAnnounce, "💠")
        while HeistPrep and HeistCount < 4:
            JoinHeist = await self.client.wait_for_reaction(["🌐","💠"], message=HeistAnnounce)
            if str(JoinHeist.reaction.emoji) == "🌐" and JoinHeist.user.id not in HeistMemID:
                if not sql.CheckUserExist(u=JoinHeist.user.id, s=ctx.message.server.id):
                    sql.NewBankUser(u=JoinHeist.user.id, s=ctx.message.server.id)
                HeistMemName.append(JoinHeist.user.name)
                HeistMemID.append(JoinHeist.user.id)
                HeistCount += 1
                HeistNChance = 0.11 + Booster(JoinHeist.user.id)
                HeistChance = HeistChance + HeistNChance
                if HeistCount == 4:
                    msg = "**Heist**\n\n**Joined Players:** \n{}\n{}/4\n\n**HeistChance:** {}%\n\n**Heist Payout:** $ {:,}\n\n**Join Now:** ***STARTING***".format(" ".join(HeistMemName), HeistCount, int(HeistChance*100), int(HeistPot/HeistCount))
                    em = dmbd.econembed(msg)
                    await self.client.edit_message(HeistAnnounce, embed=em)
                else:
                    msg = "**Heist**\n\n**Joined Players:** \n{}\n{}/4\n\n**HeistChance:** {}%\n\n**Heist Payout:** $ {:,}\n\n**Join Now:** 🌐".format(" ".join(HeistMemName), HeistCount, int(HeistChance*100), int(HeistPot/HeistCount))
                    em = dmbd.econembed(msg)
                    await self.client.edit_message(HeistAnnounce, embed=em)
            elif str(JoinHeist.reaction.emoji) == "💠" and JoinHeist.user.id == ctx.message.author.id:
                HeistPrep = False
                msg = "**Heist**\n\n**Joined Players:** \n{}\n{}/4\n\n**HeistChance:** {}%\n\n**Heist Payout:** $ {:,}\n\n**Join Now:** ***STARTING***".format(" ".join(HeistMemName), HeistCount, int(HeistChance*100), int(HeistPot/HeistCount))
                em = dmbd.econembed(msg)
                await self.client.edit_message(HeistAnnounce, embed=em)

        HeistLuck = random.randint(0,100)
        if HeistLuck <= (HeistChance * 100):
            cash = HeistPot/HeistCount
            msg = "**Heist**\n\n**Joined Players:** \n{}\n{}/4\n\n**HeistChance:** {}%\n\n**Heist Payout:** $ {:,}\n\n**Outcome:** ***SUCCESS***".format(" ".join(HeistMemName), HeistCount, int(HeistChance*100), int(HeistPot/HeistCount))
            em = dmbd.econembed(msg)
            await self.client.edit_message(HeistAnnounce, embed=em)
            await self.client.say(embed=em)
            for y in HeistMemID:
                sql.ChangeMoney(u=y, s=ctx.message.server.id, m=cash, t="cash")
                sql.ChangeMoney(u=y, s=ctx.message.server.id, m=cash, t="total")
        else:
            msg = "**Heist**\n\n**Joined Players:** \n{}\n{}/4\n\n**HeistChance:** {}%\n\n**Heist Payout:** $ {:,}\n\n**Outcome:** ***FAILED***".format(" ".join(HeistMemName), HeistCount, int(HeistChance*100), int(HeistPot/HeistCount))
            em = dmbd.econembed(msg)
            await self.client.edit_message(HeistAnnounce, embed=em)
            await self.client.say(embed=em)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def bankhack(self, ctx, user: discord.User):
        if not sql.CheckUserExist(u=ctx.message.author.id, s=ctx.message.server.id):
            sql.NewBankUser(u=ctx.message.author.id, s=ctx.message.server.id)
        if not (user == ctx.message.author):
            right = random.randint(0,3)
            code1 = id_generator(3, "AZERTYUIOPQSDFGHJKLMWXCVBN123456789")
            code2 = id_generator(3, "AZERTYUIOPQSDFGHJKLMWXCVBN123456789")
            code3 = id_generator(3, "AZERTYUIOPQSDFGHJKLMWXCVBN123456789")
            code4 = id_generator(3, "AZERTYUIOPQSDFGHJKLMWXCVBN123456789")
            passw = ["dead","bank","hell","cats"]
            pass1 = random.randint(0,3)
            pass2 = random.randint(0,3)
            pass3 = random.randint(0,3)
            pass4 = random.randint(0,3)
            msg = "{}{}\n{}{}\n{}{}\n{}{}".format(code1, passw[pass1], passw[pass2], code2, passw[pass3], code3, code4, passw[pass4])
            em = dmbd.hackembed(msg)
            Terminal = await self.client.say(embed=em)
            print(passw[right])
            TerminalA = await self.client.wait_for_message(author=ctx.message.author)
            if TerminalA:
                if TerminalA.content.lower() == passw[right]:
                    bank = sql.Hack(u=user.id, s=ctx.message.server.id)
                    if bank > 0:
                        sql.ChangeMoney(u=ctx.message.author.id, s=ctx.message.server.id, m=bank, t="cash")
                        sql.ChangeMoney(u=ctx.message.author.id, s=ctx.message.server.id, m=bank, t="total")
                        msg = "**You successfully hacked {} and took `$ {:,}`.**".format(user.mention, bank)
                        await self.client.say(msg)
                    else:
                        msg = "`{}` **isn't worth hacking.**".format(user.name)
                        await self.client.say(msg)
                else:
                    msg = "**hacking failed.**".format(user.mention)
                    await self.client.say(msg)
        else:
            msg = "**You can't hack yourself.**"
            await self.client.say(msg)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def pimp(self, ctx):
        if not sql.CheckUserExist(u=ctx.message.author.id, s=ctx.message.server.id):
            sql.NewBankUser(u=ctx.message.author.id, s=ctx.message.server.id)
        pimped = random.randint(1,50)
        sql.ChangePimped(u=ctx.message.author.id, s=ctx.message.server.id, a=pimped)
        msg = "**You pimped `{}` girls.**".format(pimped)
        await self.client.say(msg)

#VIP Commands
    @commands.command(pass_context=True)
    async def depositall(self,ctx):
        if checks.checkvip(ctx.message):
            if not sql.CheckUserExist(u=ctx.message.author.id, s=ctx.message.server.id):
                sql.NewBankUser(u=ctx.message.author.id, s=ctx.message.server.id)
            cash = sql.GetBalance(u=ctx.message.author.id, s=ctx.message.server.id)[0]
            sql.ChangeMoney(u=ctx.message.author.id, s=ctx.message.server.id, m=cash, t="bank")
            sql.ChangeMoney(u=ctx.message.author.id, s=ctx.message.server.id, m=-cash, t="cash")
            msg = "**You deposited `$ {:,}` into your bank account.**".format(cash)
            await self.client.say(msg)
        else:
            msg = "**Only VIP's can use this command.**"
            await self.client.say(msg)


def setup(client):
    client.add_cog(Bank(client))
