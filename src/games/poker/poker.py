#!usr/bin/env python3.7
#-*-coding:utf-8-*-

import discord
from discord.ext import commands
import asyncio
import logging

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
    # check if ready
    await ctx.channel.send("A new game will start soon !")
    await asyncio.sleep(0.5)
    kicklist = []
    for i in lobby.player.keys():
        chk = lambda m: m.author == i and m.channel == ctx.message.channel and m.content.lower() == 'ready'
        await ctx.channel.send("{} Answer `ready` if you are ready".format(i.mention))
        ready, message = await ask(ctx, chk, bot)
        if not ready:
            if kickifnotready:
                await lobby.leave(i,False)
                kicklist.append(i)
            else:
                await ctx.channel.send("Some players are not ready, the game won't start")
                return
    for i in kicklist: del(lobby.player[i])
    if len(lobby.player) <= 1:
        await ctx.channel.send("The game won't start, no enough remaining players in lobby")
        return
    logger.log(logging.DEBUG+1, "poker game starts in lobby %s",str(lobby.channel))

    # launch game - 1st turn
    newgame = lobby.startround()
    for i,k in newgame.cards.items():
        await i.send("Your current cards are `{}` and `{}`".format(k[0],k[1]))
    chk = lambda m: m.author == newgame.playing and m.channel == ctx.message.channel and (m.content.lower() == 'fold' or m.content.lower() == 'follow' or m.content.lower().startswith('raise '))
    await ctx.channel.send("Start of the game !")
    await asyncio.sleep(0.5)
    newtour = False
    while not newtour:
        await ctx.channel.send("{} it's your turn, reply by `fold`, `follow` or `raise [amount]`".format(newgame.playing.mention))
        answered, message = await ask(ctx, chk, bot)
        if not answered or message.content.lower() == 'fold':
            newtour = await newgame.fold(newgame.playing)
            remainsplayer = await newgame.check_remains_player()
            if not remainsplayer: return
        elif message.content.lower().startswith('raise'):
            if message.content.lower().replace('raise',"").replace(" ","").isdecimal():
                amount = int(message.content.lower().replace('raise',"").replace(" ",""))
            else: amount = 10
            newtour = await newgame.raise_(newgame.playing, amount)
        else:
            newtour = await newgame.follow(newgame.playing)
    await newgame.endturn()

    # 2nd / 3rd / 4th turn
    chk = lambda m: m.author == newgame.playing and m.channel == ctx.message.channel and (m.content.lower() == 'fold' or m.content.lower() == 'follow' or m.content.lower().startswith('raise ') or m.content.lower() == 'check')
    for i in range(3):
        await asyncio.sleep(0.5)
        newtour = False
        while not newtour:
            await ctx.channel.send("{} it's your turn, reply by `fold`, `check`, `follow` or `raise [amount]`".format(newgame.playing.mention))
            answered, message = await ask(ctx, chk, bot)
            if not answered or message.content.lower() == 'fold':
                newtour = await newgame.fold(newgame.playing)
                remainsplayer = await newgame.check_remains_player()
                if not remainsplayer: return
            elif message.content.lower().startswith('raise'):
                if message.content.lower().replace('raise',"").replace(" ","").isdecimal():
                    amount = int(message.content.lower().replace('raise',"").replace(" ",""))
                else: amount = 10
                newtour = await newgame.raise_(newgame.playing, amount)
            else:
                newtour = await newgame.follow(newgame.playing)
        await newgame.endturn()
        logger.log(logging.DEBUG+1, "poker game end in lobby %s",str(lobby.channel))
