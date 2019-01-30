
# -*- coding: utf8 -*-
import asyncio
import random
from time import strftime
import discord
from discord.ext import commands
import tools.discordembed as dmbd

class Fun:

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def rtd(self, ctx, *, dice: str ='1d6'):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except ValueError:
            await self.client.say('Format has to be in NdN!')
            return

        author = ctx.message.author
        title = 'Here are your dice results!'
        em = dmbd.newembed(author, title)
        for r in range(rolls):
            em.add_field(name="Dice #" + str(r+1), value=str(random.randint(1, limit)))
        # result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await self.client.say(embed=em)


    @commands.command(pass_context=True)
    async def flip(self, ctx):
        """ Flips a coin."""
        author = ctx.message.author

        coin = random.randint(1, 2)
        if coin == 1:
            title = "HEAD"
            em = dmbd.newembed(author, title)
            em.set_image(url="https://media.liamd.pw/MyNameIsJeff/head.png")
            await self.client.say(embed=em)
        elif coin == 2:
            title = "TAIL"
            em = dmbd.newembed(author, title)
            em.set_image(url="https://media.liamd.pw/MyNameIsJeff/tail.png")
            await self.client.say(embed=em)


    @commands.command(pass_context=True, description='Ask the client to choose one')
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple choices."""
        author = ctx.message.author
        em = dmbd.newembed(author, random.choice(choices))
        await self.client.say(embed=em)

    @commands.command(pass_context=True, name='8ball')
    async def ball(self, ctx, *, question: str):
        """ Ask the 8Ball """
        answers = ['It is certain', 'It is decidedly so', 'Without a doubt',
                   'Yes, definitely', 'You may rely on it', 'As I see it, yes',
                   'Most likely', 'Outlook good', 'Yes', 'Signs point to yes',
                   'Reply hazy try again', 'Ask again later',
                   'Better not tell you now', 'Cannot predict now',
                   'Concentrate and ask again', 'Don\'t count on it',
                   'My reply is no', 'My sources say no',
                   'Outlook not so good', 'Very doubtful']

        author = ctx.message.author
        em = dmbd.newembed(author, random.choice(answers))
        await self.client.say(embed=em)

    @commands.command()
    async def yourpowers(self):
        """ ADRENALINE IS PUMPING """
        await self.client.say("Ehm, Idk ?!?!!???")

def setup(client):
    client.add_cog(Fun(client))
