#!usr/bin/env python3.7
#-*-coding:utf-8-*-

from discord.ext import commands
from src.discord.checks import *
from src.discord.converters import *
from src.discord.database.database import *
from src.discord.database.table import *
from src.games.poker.lobby import *
from src.games.poker.poker import *
from src.games.pennymachine import *
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
        bet = abs(bet)
        color, number = area
        validColor, validNumber = choice(["red","black"]), randint(0,18)
        db = Database(self.bot,self.logger,ctx.guild.id,"selfguild")
        usertable = Table(db,"user")
        users = await usertable.fetch()
        for user in users:
            if user[0] == str(ctx.author.id): break
        for srvind in users:
            if "-1" == srvind[0]: break
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
            await ctx.channel.send("You win ! you have earned : {} coins".format((bet*10) - int(srvind[1])))
            coins += ((bet*10) - int(srvind[1]))
        else:
            await ctx.channel.send("You lose !")
        await usertable.update_row(user[0],str(coins))

    @commands.check(check_inserv)
    @commands.group(invoke_without_command=False)
    async def poker(self, ctx): pass

    @poker.group(name="lobby", invoke_without_command=False)
    async def poker_lobby(self, ctx): pass

    @poker_lobby.command(name="create", aliases=["+","new"])
    async def poker_lobby_create(self, ctx, name, buy_in: int, round: typing.Optional[int] = 10):
        """Create a lobby for playing poker game. Other players could join with `/poker lobby join`"""
        buy_in = abs(buy_in)
        cat = discord.utils.get(ctx.guild.categories, name="poker")
        chan = None
        if cat is None:
            everyoneperm = discord.PermissionOverwrite(read_messages=False, send_messages=False,
                        manage_messages=False,
                        read_message_history=False)
            perms = {ctx.guild.default_role: everyoneperm}
            cat = await ctx.guild.create_category_channel("poker",overwrites=perms,reason="creating poker category")
            self.logger.info("creating poker category")
        else:
            chan = discord.utils.get(cat.text_channels, name=name)
            if chan is not None:
                await ctx.channel.send("This lobby already exists, join it or create another lobby")
                return
        chan = await ctx.guild.create_text_channel(name, category=cat, reason="creating poker lobby", slowmode_delay=5)
        lobby = PokerLobby(ctx.author, chan, buy_in, self.bot, self.logger, round)
        await lobby.join(ctx.author)

    @commands.check(check_inpokerlobby)
    @commands.check(check_pokerlobbyowner)
    @poker_lobby.command(name="disband", aliases=["-","delete","remove"])
    async def poker_lobby_disband(self, ctx):
        """Disband the current lobby, you'll need to be the owner of the lobby"""
        lobby = PokerLobby.instances[ctx.channel]
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
        """Join an existing poker lobby"""
        await lobby.join(ctx.author)

    @commands.check(check_inpokerlobby)
    @poker_lobby.command(name="leave")
    async def poker_lobby_leave(self, ctx):
        """Leave the lobby where you are"""
        lobby = PokerLobby.instances[ctx.channel]
        await lobby.leave(ctx.author)
        if lobby.owner == ctx.author:
            if len(lobby.player) == 0:
                await lobby.disband()
            else:
                lobby.owner = list(lobby.player.keys())[0]

    @commands.check(check_inpokerlobby)
    @commands.check(check_pokerlobbyowner)
    @poker.command(name="start")
    async def poker_start(self, ctx, kickifnotready: typing.Optional[bool] = False):
        """Start a poker game in the current lobby"""
        lobby = PokerLobby.instances[ctx.channel]
        await game(ctx, self.bot, self.logger, lobby, kickifnotready)
        await asyncio.sleep(5)
        await lobby.check_auto_disband()

    @commands.check(check_inserv)
    @commands.command()
    async def pennymachine(self, ctx, bet: int):
        """Make your bet and pray for the win"""
        await pennymachine_game(self.bot, self.logger, ctx, bet)
