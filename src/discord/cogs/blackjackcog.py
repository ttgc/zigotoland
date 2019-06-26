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
import random

class Blackjack(commands.Cog):
    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger

    @commands.check(check_inserv)
    @commands.command()
    async def blackjack(self, ctx, bet: int)
        """Make your bet and beat the bank"""
        deck = [1,2,3,4,5,6,7,8,9,10,'J','Q','K']*4
        player_hand = []
        dealer_hand = []
        random.shuffle(deck)
        for i in range(0, 3, 2):
            player_hand.append(deck[i])
            dealer_hand.append(deck[i+1])

        await ctx.channel.send("votre main: "+ player_hand))
        
