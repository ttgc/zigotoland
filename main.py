#!usr/bin/env python3.7
#-*-coding:utf-8-*-

# import external and python libraries
import discord
from discord.ext import commands
import asyncio
import logging
import os
import json

# import personal libraries
from src.logs import *

# import cogs
from src.discord.cogs.utils import *

# =============== INIT ===============

# logger init
global logger
logger = initlogs()

# config init
global config
with open("config.json","r") as configfile:
    config = json.load(config)
# token init
global TOKEN
TOKEN = config["token"]

# client init
global client
client = discord.ext.commands.Bot('/',case_insensitive=True)

# self-managed guild init
global SELF_GUILD
SELF_GUILD = None
if config["self-guild"].get("mode","load") == "load":
    SELF_GUILD = config["self-guild"]["ID"]

# =============== CORE ===============

# events
@client.event
async def on_guild_available(guild):
    global SELF_GUILD, logger, client
    if guild == SELF_GUILD:
        logger.warning("The self managed guild has become avalaible again, reconnecting, and enabling bot")
        for cogname, cog in client.cogs:
            if cogname != "Utils":
                for cmd in cog.get_commands():
                    cmd.update(enabled=True)

@client.event
async def on_guild_unavailable(guild):
    global SELF_GUILD, logger, client
    if guild == SELF_GUILD:
        logger.warning("The self managed guild has become unavalaible, waiting for reconnect, and disabling bot")
        for cogname, cog in client.cogs:
            if cogname != "Utils":
                for cmd in cog.get_commands():
                    cmd.update(enabled=False)

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

# =============== MAIN ===============
async def main():
    global TOKEN
    client.add_cog(Utils(client,logger))
    await client.login(TOKEN)
    await client.connect()

# ================ RUN ================
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
except:
    loop.run_until_complete(client.logout())
finally:
    loop.close()
