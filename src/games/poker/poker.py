#!usr/bin/env python3.7
#-*-coding:utf-8-*-

import discord
from discord.ext import commands
import asyncio

from src.games.poker.cardset import CardSet, Card
from src.games.poker.lobby import PokerLobby
from src.games.poker.round import PokerRound

async def ask(ctx, chk, bot):
    try: answer = await bot.wait_for('message',check=chk,timeout=60)
    except asyncio.TimeoutError: answer = None
    if answer is None:
        await ctx.message.channel.send("your request has timeout")
        return False, None
    return True, answer

async def game(ctx, bot, logger, lobby, kickifnotready=True):
    answers = {}

    async def setready(chk, player):
        answers[player], message = ask(ctx, chk, bot)

    async def askready():
        for player in lobby.player:
            chk = lambda m: m.author == player and m.channel == ctx.message.channel and m.content.lower() == 'ready'
            asyncio.run_coroutine_threadsafe(setready(chk, player), bot.loop)

    # check if ready
    await ctx.channel.send("A new game will start soon ! Please answer `ready` to confirm")
    try: asyncio.wait_for(askready(), 65.0, loop=bot.loop)
    except asyncio.TimeoutError: pass
    kicklist = []
    for i in lobby.player.items():
        if answers.get(i, None) is None or not answers[i]:
            if kickifnotready:
                await lobby.leave(i,False)
                kicklist.append(i)
            else:
                await ctx.channel.send("Some players are not ready, the game won't start")
                return
    for i in kicklist: del(lobby.player[i])

    # launch game - 1st turn
    newgame = lobby.startround()
    chk = lambda m: m.author == lobby.playing and m.channel == ctx.message.channel and (m.content.lower() == 'fold' or m.content.lower() == 'follow' or m.content.lower().startswith('raise '))
    await ctx.channel.send("Start of the game !")
    await asyncio.sleep(0.5)
    newtour = False
    while not newtour:
        await ctx.channel.send("{} it's your turn, reply by `fold`, `follow` or `raise [amount]`".format(newgame.playing.mention))
        answered, message = await ask(ctx, chk, bot)
        if not answered or message.content.lower() == 'fold':
            newtour = await newgame.fold(lobby.playing)
        elif message.content.lower().startswith('raise'):
            if message.content.lower().replace('raise',"").replace(" ","").isdecimal():
                amount = int(message.content.lower().replace('raise',"").replace(" ",""))
            else: amount = 10
            newtour = await newgame.raise_(lobby.playing, amount)
        else:
            newtour = await newgame.follow(lobby.playing)
    await newgame.endturn()

    # 2nd / 3rd / 4th turn
    chk = lambda m: m.author == lobby.playing and m.channel == ctx.message.channel and (m.content.lower() == 'fold' or m.content.lower() == 'follow' or m.content.lower().startswith('raise ') or m.content.lower() == 'check')
    for i in range(3):
        await asyncio.sleep(0.5)
        newtour = False
        while not newtour:
            await ctx.channel.send("{} it's your turn, reply by `fold`, `check`, `follow` or `raise [amount]`".format(newgame.playing.mention))
            answered, message = await ask(ctx, chk, bot)
            if not answered or message.content.lower() == 'fold':
                newtour = await newgame.fold(lobby.playing)
            elif message.content.lower().startswith('raise'):
                if message.content.lower().replace('raise',"").replace(" ","").isdecimal():
                    amount = int(message.content.lower().replace('raise',"").replace(" ",""))
                else: amount = 10
                newtour = await newgame.raise_(lobby.playing, amount)
            else:
                newtour = await newgame.follow(lobby.playing)
        await newgame.endturn()
