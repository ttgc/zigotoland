#!usr/bin/env python3.7
#-*-coding:utf-8-*-

import discord
from discord.ext import commands
import asyncio
import logging
import os
import json
import typing
import emojis #pip3 install -U emojis

from src.discord.cogs.utils import *
from src.discord.cogs.PennyMachineCog import *

from src.logs import *


global logger
logger = initlogs()

global TOKEN
with open("config.json","r") as config:
    TOKEN = json.load(config)["token"]

global client
client = discord.ext.commands.Bot('/',case_insensitive=True)

# Code here

@client.event
async def on_ready():
    global logger
    logger.info("Successful connected. Initializing bot system")
    botaskperm = discord.Permissions().all()
    botaskperm.administrator = botaskperm.manage_channels = botaskperm.manage_guild = botaskperm.manage_webhooks = botaskperm.manage_emojis = botaskperm.manage_nicknames = botaskperm.move_members = False
    url = discord.utils.oauth_url(str(client.user.id),botaskperm)
    print(url)
    logger.info("Generate invite link : %s",url)
    logger.info("Bot is now ready")

async def main():
    global TOKEN
    client.add_cog(Utils(client,logger))
    client.add_cog(PennyMachines(client, logger))
    await client.login(TOKEN)
    await client.connect()

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())

except:
    loop.run_until_complete(client.logout())
finally:
    loop.close()
