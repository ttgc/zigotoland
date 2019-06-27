#!usr/bin/env python3.7
#-*-coding:utf-8-*-

from src.utils.config import *
from src.games.poker.lobby import *

def check_botowner(ctx):
    config = Config()
    return ctx.author.id in config.owners

def check_inserv(ctx):
    config = Config()
    return (ctx.guild == config.guild)

def check_inpokerlobby(ctx):
    return ctx.channel in PokerLobby.instances
