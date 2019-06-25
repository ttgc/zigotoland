#!usr/bin/env python3.7
#-*-coding:utf-8-*-

# import external and python libraries
import discord
from discord.ext import commands
import asyncio
import logging
import os, sys

# import personal libraries
from src.utils.logs import *
from src.utils.config import *

# import cogs
from src.discord.cogs.utils import *

# =============== INIT ===============

# logger init
global logger
logger = initlogs()

# config init
global config
config = Config()

# token init
global TOKEN
TOKEN = config.token

# client init
global client
client = discord.ext.commands.Bot('/',case_insensitive=True)

# =============== CORE ===============

# events
@client.event
async def on_guild_available(guild):
    global logger, client, config
    if guild == config.guild:
        logger.warning("The self managed guild has become avalaible again, reconnecting, and enabling bot")
        for cogname, cog in client.cogs:
            if cogname != "Utils":
                for cmd in cog.get_commands():
                    cmd.update(enabled=True)

@client.event
async def on_guild_unavailable(guild):
    global logger, client, config
    if guild == config.guild:
        logger.warning("The self managed guild has become unavalaible, waiting for reconnect, and disabling bot")
        for cogname, cog in client.cogs:
            if cogname != "Utils":
                for cmd in cog.get_commands():
                    cmd.update(enabled=False)

@client.event
async def on_member_join(member):
    global logger, client, config
    if member.guild == config.guild and member.id in config.owners:
        await member.add_roles(config.adminrole, reason="Assigned admin role to owner")
        logger.info("Assigned admin role to owner in self guild")

@client.event
async def on_ready():
    global logger, client, config
    # Bot invite link
    logger.info("Successful connected. Initializing bot system")
    botaskperm = discord.Permissions().all()
    botaskperm.administrator = botaskperm.manage_channels = botaskperm.manage_guild = botaskperm.manage_webhooks = botaskperm.manage_emojis = botaskperm.manage_nicknames = botaskperm.move_members = False
    url = discord.utils.oauth_url(str(client.user.id),botaskperm)
    print(url)
    logger.info("Generate invite link : %s",url)

    # Self guild load/creation
    if config.guildID is None:
        with open("pictures/guild-logo.png","rb") as avatar:
            guild = await client.create_guild("Financial District", config.guildRegion, avatar.read())
        await guild.create_role(name="Masakaki", permissions=discord.Permissions.all(),
                                color=discord.Color(int("CE618E",16)), hoist=True,
                                mentionable=True, reason="Creating admin role")
        logger.info("self guild %d created successful", guild.id)
    else:
        guild = discord.utils.get(client.guilds, id=config.guildID)
        if guild is None:
            logger.critical("unavalaible guild specified in config.json")
            await client.logout()
            sys.exit(1)
        logger.info("self guild loaded successful")
    config.initGuild(guild)

    # Self guild management
    invite = await guild.text_channels[0].create_invite(max_uses=1,reason="Create admin invite")
    logger.info("Created invite to self-guild : %s",invite.url)
    print(invite.url)

    logger.info("Bot is now ready")

# =============== MAIN ===============
async def main():
    global TOKEN, logger, client
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
