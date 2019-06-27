import typing
import discord
import logging
import asyncio
import math
import random
from discord.ext import commands
from src.discord.checks import *
from src.discord.converters import *
from src.discord.database.database import *
from src.discord.database.table import *


client = discord.Client()

class Pennymachine(commands.Cog):

    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger

    @commands.check(check_inserv)
    @commands.command()
    async def pennymachine(self, ctx, bet: int ):
        """Make your bet and pray for the win"""

        money_up1 = 0
        money_up2 = 2
        money_up3 = 4
        money_up4 = 6
        money_up5 = 10
        money_up6 = 100
        money_up7 = 1000
        money_down1 = -7
        money_down2 = -6
        money_down3 = -5
        money_down4 = -4
        money_down5 = -3
        money_down6 = -2
        money_down7 = -1
        full_lose = -10

        db = Database(self.bot,self.logger,ctx.guild.id,"selfguild")
        usertable = Table(db,"user")
        users = await usertable.fetch()
        for user in users:
            if user[0] == str(ctx.author.id): break
        coins = int(user[1]) - bet

        draw1, draw2, draw3 = 0, 0, 0
        list = [random.randint(1, 100), random.randint(1, 100), random.randint(1, 100)]
        draw1, draw2, draw3 = list[0], list[1], list[2]

        if list[0] < 5:
            draw1 = 7
        elif list[0] < 10:
            draw1 = 6
        elif list[0] < 20:
            draw1 = 5
        elif list[0] < 35:
            draw1 = 4
        elif list[0] < 55:
            draw1 = 3
        elif list[0] < 75:
            draw1 = 2
        else:
            draw1 = 1

        if list[1] < 5:
            draw2 = 7
        elif list[1] < 10:
            draw2 = 6
        elif list[1] < 20:
            draw2 = 5
        elif list[1] < 35:
            draw2 = 4
        elif list[1] < 55:
            draw2 = 3
        elif list[1] < 75:
            draw2 = 2
        else:
            draw2 = 1

        if list[2] < 5:
            draw3 = 7
        elif list[2] < 10:
            draw3 = 6
        elif list[2] < 20:
            draw3 = 5
        elif list[2] < 35:
            draw3 = 4
        elif list[2] < 55:
            draw3 = 3
        elif list[2] < 75:
            draw3 = 2
        else:
            draw3 = 1
        await ctx.channel.send(draw1)
        await ctx.channel.send(draw2)
        await ctx.channel.send(draw3)

        await asyncio.sleep(0.2)
        if draw1 == 1:
            await ctx.channel.send(":poop:")
        elif draw1 == 2:
            await ctx.channel.send(":monkey_face:")
        elif draw1 == 3:
            await ctx.channel.send(":banana:")
        elif draw1 == 4:
            await ctx.channel.send(":watermelon:")
        elif draw1 == 5:
            await ctx.channel.send(":cherries:")
        elif draw1 == 6:
            await ctx.channel.send(":kiwi:")
        else:
            await ctx.channel.send(":moneybag:")

        if draw2 == 1:
            await ctx.channel.send(":poop:")
        elif draw2 == 2:
            await ctx.channel.send(":monkey_face:")
        elif draw2 == 3:
            await ctx.channel.send(":banana:")
        elif draw2 == 4:
            await ctx.channel.send(":watermelon:")
        elif draw2 == 5:
            await ctx.channel.send(":cherries:")
        elif draw2 == 6:
            await ctx.channel.send(":kiwi:")
        else:
            await ctx.channel.send(":moneybag:")

        if draw3 == 1:
            await ctx.channel.send(":poop:")
        elif draw3 == 2:
            await ctx.channel.send(":monkey_face:")
        elif draw3 == 3:
            await ctx.channel.send(":banana:")
        elif draw3 == 4:
            await ctx.channel.send(":watermelon:")
        elif draw3 == 5:
            await ctx.channel.send(":cherries:")
        elif draw3 == 6:
            await ctx.channel.send(":kiwi:")
        else:
            await ctx.channel.send(":moneybag:")


        if draw1 == draw2 and draw2 == draw3:
            if draw1 == 7:
                await ctx.channel.send("You win ! you have earned : {} coins".format(bet*money_up7))
                coins += (bet*money_up7)
            elif draw1 == 6:
                await ctx.channel.send("You win ! you have earned : {} coins".format(bet*money_up6))
                coins += (bet*money_up6)
            elif draw1 == 5:
                await ctx.channel.send("You win ! you have earned : {} coins".format(bet*money_up5))
                coins += (bet*money_up5)
            elif draw1 == 4:
                await ctx.channel.send("You win ! you have earned : {} coins".format(bet*money_up4))
                coins += (bet*money_up4)
            elif draw1 == 3:
                await ctx.channel.send("You win ! you have earned : {} coins".format(bet*money_up3))
                coins += (bet*money_up3)
            elif draw1 == 2:
                await ctx.channel.send("You win ! you have earned : {} coins".format(bet*money_up2))
                coins += (bet*money_up2)
            elif draw1 == 1:
                await ctx.channel.send("You win ! you have earned : {} coins".format(bet*money_up1))
                coins += (bet*money_up1)
        elif draw1 == draw2 or draw1 == draw3 or draw2 == draw3:
            if draw1 == 7:
                await ctx.channel.send("You win ! you have lost : {} coins".format(bet*money_down7))
                coins += (bet*money_down5)
            elif draw1 == 6:
                await ctx.channel.send("You win ! you have lost : {} coins".format(bet*money_down6))
                coins += (bet*money_down5)
            elif draw1 == 5:
                await ctx.channel.send("You win ! you have lost : {} coins".format(bet*money_down5))
                coins += (bet*money_down5)
            elif draw1 == 4:
                await ctx.channel.send("You win ! you have lost : {} coins".format(bet*money_down4))
                coins += (bet*money_down4)
            elif draw1 == 3:
                await ctx.channel.send("You win ! you have lost : {} coins".format(bet*money_down3))
                coins += (bet*money_down3)
            elif draw1 == 2:
                await ctx.channel.send("You win ! you have lost : {} coins".format(bet*money_down2))
                coins += (bet*money_down2)
            elif draw1 == 1:
                await ctx.channel.send("You win ! you have lost : {} coins".format(bet*money_down1))
                coins += (bet*money_down1)
        else:
            await ctx.channel.send("You lose ! you have lost : {} coins".format(bet*full_lose))
            coins += (bet*full_lose)

        await usertable.update_row(user[0],str(coins))
