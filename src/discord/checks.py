#!usr/bin/env python3.7
#-*-coding:utf-8-*-

from src.utils.config import *
from src.games.poker.lobby import *
from src.discord.manage import *
from src.utils.logs import getlogger

def check_botowner(ctx):
    config = Config()
    return ctx.author.id in config.owners

def check_inserv(ctx):
    config = Config()
    return (ctx.guild == config.guild)

def check_inpokerlobby(ctx):
    return ctx.channel in PokerLobby.instances

def check_pokerlobbyowner(ctx):
    if not check_inpokerlobby(ctx): return False
    return PokerLobby.instances[ctx.channel].owner == ctx.author

async def check_darkmember(ctx):
    if not check_inserv(ctx): return False
    logger = getlogger()
    gold, plat, dark = await manage_roles(ctx, logger)
    return dark in ctx.author.roles
