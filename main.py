#!usr/bin/env python3.7
#-*-coding:utf-8-*-

import discord
from discord.ext import commands
import asyncio
import logging
import os
import json

from src.logs import *

global logger
logger = initlogs()

global TOKEN
with open("config.json","r") as config:
    TOKEN = json.load(config)["token"]

global client
client = discord.ext.commands.Bot('/',case_insensitive=True)

# Code here

async def main():
    global TOKEN
    await client.login(TOKEN)
    await client.connect()

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
except:
    loop.run_until_complete(client.logout())
finally:
    loop.close()
