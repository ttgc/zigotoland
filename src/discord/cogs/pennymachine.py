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

        money_up1 = 0.5
        money_up2 = 1
        money_up3 = 2
        money_up4 = 4
        money_up5 = 8
        money_up6 = 10
        money_up7 = 1000

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


        if draw1 == 1:
            res1 = ":poop:"
        elif draw1 == 2:
            res1 = ":monkey_face:"
        elif draw1 == 3:
            res1 = ":banana:"
        elif draw1 == 4:
            res1 = ":watermelon:"
        elif draw1 == 5:
            res1 = ":cherries:"
        elif draw1 == 6:
            res1 = ":kiwi:"
        else:
            res1 = ":moneybag:"

        if draw2 == 1:
            res2 = ":poop:"
        elif draw2 == 2:
            res2 = ":monkey_face:"
        elif draw2 == 3:
            res2 = ":banana:"
        elif draw2 == 4:
            res2 = ":watermelon:"
        elif draw2 == 5:
            res2 = ":cherries:"
        elif draw2 == 6:
            res2 = ":kiwi:"
        else:
            res2 = ":moneybag:"

        if draw3 == 1:
            res3 = ":poop:"
        elif draw3 == 2:
            res3 = ":monkey_face:"
        elif draw3 == 3:
            res3 = ":banana:"
        elif draw3 == 4:
            res3 = ":watermelon:"
        elif draw3 == 5:
            res3 = ":cherries:"
        elif draw3 == 6:
            res3 = ":kiwi:"
        else:
            res3 = ":moneybag:"

        available = [":poop:",":monkey_face:",":banana:",":watermelon:",":cherries:",":kiwi:",":moneybag:"]
        iteration = random.randint(5,15)
        init = "{}{}{}".format(random.choice(available), random.choice(available), random.choice(available))
        msg = await ctx.channel.send(content = init)
        while (iteration > 0):
            rolling = "{}{}{}".format(random.choice(available), random.choice(available), random.choice(available))
            await msg.edit(content = rolling)
            await asyncio.sleep(0.2)
            iteration -= 1

        await asyncio.sleep(0.5)
        final_res = "{}{}{}".format(res1, res2, res3)
        await ctx.channel.edit(content=final_res)

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
        else:
            await ctx.channel.send("You lose !")

        await usertable.update_row(user[0],str(coins))
