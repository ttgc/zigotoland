#!usr/bin/env python3.7
#-*-coding:utf-8-*-

import discord.utils
import json

def check_botowner(ctx):
    with open("config.json","r") as configfile:
        config = json.load(configfile)
    return ctx.author.id in config["owner"]
