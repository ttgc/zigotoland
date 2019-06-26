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
import typing

class Games(commands.Cog):
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
        coins = int(user[1]) - bet
        avalaible = ["R1","R2","R3","R4","R5","R6","R7","R8","R9","R10","R11","R12","R13","R14","R15","R16","R17","R18",
                    "B1","B2","B3","B4","B5","B6","B7","B8","B9","B10","B11","B12","B13","B14","B15","B16","B17","B18"]
        shuffle(avalaible)
        msg = await ctx.channel.send(avalaible[0])
        iteration = randint(5,15)
        while (iteration > 0):
            await msg.edit(content=avalaible[iteration%len(avalaible)])
            await asyncio.sleep(0.2)
            iteration -= 1
        formated = "{}{}".format(validColor[0].upper(), validNumber)
        await msg.edit(content=formated)
        await asyncio.sleep(1)
        if color == validColor and number == validNumber:
            await ctx.channel.send("You win ! you have earned : {} coins".format(bet*10))
            coins += (bet*10)
        else:
            await ctx.channel.send("You lose !")
        await usertable.update_row(user[0],str(coins))

    @commands.check(check_inserv)
    @commands.group(invoke_without_command=False)
    async def poker(self, ctx): pass

    @poker.group(name="lobby", invoke_without_command=False)
    async def poker_lobby(self, ctx): pass

    @poker_lobby.command(name="create", aliases=["+","new"])
    async def poker_lobby_create(self, ctx, name, initial_bet: int, round: typing.Optional[int] = 10):
        cat = discord.utils.get(ctx.guild.categories, name="poker")
        chan = None
        if cat is None:
            everyoneperm = discord.PermissionOverwrite(read_messages=False, send_messages=False,
                        manage_messages=False,
                        read_message_history=False)
            perms = {srv.default_role: everyoneperm}
            cat = await ctx.guild.create_category_channel("poker",overwrites=perms,reason="creating poker category")
            self.logger.info("creating poker category")
        else:
            chan = discord.utils.get(cat.text_channels, name=name)
            if chan is not None:
                await ctx.channel.send("This lobby already exists, join it or create another lobby")
                return
        chan = await ctx.guild.create_text_channel(name, category=cat, reason="creating poker lobby", slowmode_delay=10)
        lobby = PokerLobby(ctx.author, chan, initial_bet, self.bot, self.logger, round)
        await lobby.join(ctx.author)

    @poker_lobby.command(name="disband", aliases=["-","delete","remove"])
    async def poker_lobby_disband(self, ctx):
        lobby = PokerLobby.instances.get(ctx.channel, None)
        if lobby is None:
            await ctx.channel.send("this channel is not a poker lobby")
        elif lobby.owner != ctx.author:
            await ctx.channel.send("you are not the owner of this lobby")
        else:
            await ctx.message.channel.send("Do you really to disband the lobby ? This cannot be undone ! Type `confirm` to disband it")
            chk = lambda m: m.author == ctx.message.author and m.channel == ctx.message.channel and m.content.lower() == 'confirm'
            try: answer = await self.bot.wait_for('message',check=chk,timeout=60)
            except asyncio.TimeoutError: answer = None
            if answer is None:
                await ctx.message.channel.send("your request has timeout")
            else:
                await lobby.disband()

    @poker_lobby.command(name="join")
    async def poker_lobby_join(self, ctx, lobby: LobbyConverter):
        await lobby.join(ctx.author)

    @poker_lobby.command(name="leave")
    async def poker_lobby_leave(self, ctx):
        lobby = PokerLobby.instances.get(ctx.channel, None)
        if lobby is None:
            await ctx.channel.send("this channel is not a poker lobby")
        else:
            await lobby.leave(ctx.author)
