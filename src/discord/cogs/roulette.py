#!usr/bin/env python3.7
#-*-coding:utf-8-*-

from discord.ext import commands
from src.discord.checks import *
from src.discord.converters import *
from src.discord.database.database import *
from src.discord.database.table import *
from random import randint, choice, shuffle
import logging
import asyncio

class Roulette(commands.Cog):
    def __init__(self,bot,logger):
        self.bot = bot
        self.logger = logger

    @commands.check(check_inserv)
    @commands.command()
    async def roulette(self,ctx,bet: int,area: RouletteConverter):
        """Choose your color and number, and pray for winning !
        The area (color+number) is given as following : R17 for the red color and number 17
        There are 2 colors : R(ed) and B(lack)
        And there are 18 numbers from 1 to 18 included"""
        color, number = area
        validColor, validNumber = choice(["red","black"]), randint(0,18)
        db = Database(self.bot,self.logger,ctx.guild.id,"selfguild")
        usertable = Table(db,"user")
        users = await usertable.fetch()
        for user in users:
            if user[0] == str(ctx.author.id): break
        user[1] = str(int(user[1]) - bet)
        avalaible = ["R1","R2","R3","R4","R5","R6","R7","R8","R9","R10","R11","R12","R13","R14","R15","R16","R17","R18",
                    "B1","B2","B3","B4","B5","B6","B7","B8","B9","B10","B11","B12","B13","B14","B15","B16","B17","B18"]
        shuffle(avalaible)
        msg = await ctx.channel.send(avalaible[0])
        iteration = randint(20,40)
        while (iteration > 0):
            msg.edit(content=avalaible[iteration%len(avalaible)])
            await asyncio.sleep(0.25)
            iteration -= 1
        formated = "{}{}".format(validColor[0].upper(), validNumber)
        msg.edit(content=formated)
        await asyncio.sleep(1)
        if color == validColor and number == validNumber:
            await ctx.channel.send("You win ! you have earned : {} coins".format(bet*10))
            user[1] = str(user[1]+(bet*10))
        else:
            await ctx.channel.send("You lose !")
        await usertable.update_row(user[0],user[1])
