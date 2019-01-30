import asyncio
import discord
import tools.colorprint as clrp
import os

from discord.ext import commands
from discord.ext.commands import Bot

Client = discord.Client()
client = commands.Bot(command_prefix=commands.when_mentioned_or("d!"))

class General:

    def __init__(self, client):
        self.client = client

    @client.event
    async def on_member_join(member):
        if sql.WelcomeChannelSet(member.server.id):
            avatar = "https://cdn.discordapp.com/avatars/{}/{}.png".format(member.id, member.avatar)
            img = imgt.ImageWrite(imgurl=avatar, name="{}#{}".format(member.name, member.discriminator), server=member.server.name)
            await self.client.send_file(member.server.get_channel(str(sql.GetWelcomeChannel(member.server.id))), img[0])
            for y in img:
                os.remove(y)

    @client.event
    async def on_message(message):
        if not message.author.bot:
            commandtest = message.content.split("!")
            if not message.channel.is_private:
                if commandtest[0] == "d" or message.content.startswith("<@402246509313392640>"):
                    if checks.checkdev(message):
                        if sql.CheckBan(message.author.id):
                            Banmessage = "Sorry {}, you are banned from using Dragon. Want an unban ? Send a message to Flop#1536.".format(message.author.mention)
                            await self.client.send_message(message.author, Banmessage)
                            print(clrp.WARNING+"{} is banned and used the command: {}".format(message.author.name, message.content)+clrp.RESET)
                            await self.client.delete_message(message)
                        elif message.content.startswith("<@"):
                            if self.client.get_command(message.content.split()[1]):
                                await self.client.process_commands(message)
                                print(clrp.LOG+"{} used the command: {}".format(message.author.id, message.content)+clrp.RESET)
                            else:
                                #sendmessage = "I do not know the command **" + commandtest[1] + "**. Please check for typos " + message.author.name
                                await self.client.delete_message(message)
                                #await self.client.send_message(message.channel, sendmessage)
                        elif self.client.get_command(commandtest[1]):
                            await self.client.process_commands(message)
                            print(clrp.LOG+"{} used the command: {}".format(message.author.id, message.content)+clrp.RESET)
                        else:
                            #sendmessage = "I do not know the command **" + commandtest[1] + "**. Please check for typos " + message.author.name
                            await self.client.delete_message(message)
                            #await self.client.send_message(message.channel, sendmessage)

    @client.event
    async def on_command_error(error, ctx):
        if isinstance(error, commands.CommandOnCooldown):
            seconds = error.retry_after
            minutes = int(error.retry_after // 60)
            seconds = int(seconds - (minutes*60))
            if ctx.message.content.startswith('d!crime'):
                msg = 'You can commit a crime in {}m {}s'.format(minutes, seconds)
                em = dmbd.econembed(msg)
                await self.client.send_message(ctx.message.channel, embed=em)
            elif ctx.message.content.startswith('d!work'):
                msg = 'You can work in {}m {}s'.format(minutes, seconds)
                em = dmbd.econembed(msg)
                await self.client.send_message(ctx.message.channel, embed=em)
            elif ctx.message.content.startswith('d!pimp'):
                msg = 'You can pimp in {}m {}s'.format(minutes, seconds)
                em = dmbd.econembed(msg)
                await self.client.send_message(ctx.message.channel, embed=em)
            elif ctx.message.content.startswith('d!mug'):
                msg = 'You can mug someone in {}m {}s'.format(minutes, seconds)
                em = dmbd.econembed(msg)
                await self.client.send_message(ctx.message.channel, embed=em)
            elif ctx.message.content.startswith('d!heist'):
                msg = 'You can start another heist in {}m {}s'.format(minutes, seconds)
                em = dmbd.econembed(msg)
                await self.client.send_message(ctx.message.channel, embed=em)
            elif ctx.message.content.startswith('d!bankhack'):
                msg = 'You can start hacking in {}m {}s'.format(minutes, seconds)
                em = dmbd.econembed(msg)
                await self.client.send_message(ctx.message.channel, embed=em)
        else:
            print(clrp.ERROR+"==========An Error Occured=========="+clrp.RESET)
            raise error


def setup(client):
    client.add_cog(General(client))
