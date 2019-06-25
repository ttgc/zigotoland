#!usr/bin/env python3.7
#-*-coding:utf-8-*-

from src.utils.config import *

def check_botowner(ctx):
    config = Config()
    return ctx.author.id in config.owners

def check_inserv(ctx):
    return True
