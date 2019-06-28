#!usr/bin/env python3.7
#-*-coding:utf-8-*-

# import external and python libraries
import discord
from discord.ext import commands
import asyncio
import logging
import os, sys
import traceback

# import personal libraries
from src.utils.logs import *
from src.utils.config import *
from src.discord.database.database import *
from src.discord.database.table import *
from src.discord.help import *
from src.discord.manage import *

# import cogs
from src.discord.cogs.utils import *
from src.discord.cogs.games import *

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
client = discord.ext.commands.Bot('/',case_insensitive=True,help_command=Help())

# =============== CORE ===============

# invoke related events
@client.after_invoke
async def check_money(ctx):
    global logger, client, config
    if ctx.guild == config.guild:
        gold, plat, dark = await manage_roles(ctx, logger)
        db = Database(client,logger,config.guild.id,"selfguild")
        userdb = Table(db,"user")
        userlist = await userdb.fetch()
        for i in userlist:
            if int(i[0]) == ctx.author.id and int(i[1]) < 0:
                await ctx.author.send("You lose ! You are bankrupt !")
                await ctx.channel.send("{} is bankrupt and has been exiled from financial district".format(str(ctx.author)))
                await config.guild.ban(ctx.author,reason="bankrupt",delete_message_days=1)
            elif int(i[0]) == ctx.author.id:
                money = int(i[1])
                await update_member_status(ctx, money, gold, plat, dark)

# events
@client.event
async def on_command_error(ctx, error):
    global logger
    msg = "The following error has occured during the execution of your command :\n```\n{}\n```".format(error)

    if isinstance(error, commands.UserInputError) or isinstance(error, commands.ConversionError):
        msg = "Your command contains some errors, some arguments are mispelled, missing or of an incorrect type. Please check your syntax"
    elif isinstance(error, commands.CommandNotFound) or isinstance(error, commands.CheckFailure): return
    elif isinstance(error, commands.DisabledCommand):
        msg = "This command is currently disabled and cannot be called"
    elif isinstance(error, commands.CommandOnCooldown):
        msg = "This command is still in cooldown for {0:.2f} sec".format(error.retry_after)
    else: logger.warning(error)

    logger.log(logging.DEBUG+1, error)
    await ctx.channel.send(msg)

@client.event
async def on_error(event,*args,**kwargs):
    global logger
    logger.error(traceback.format_exc())

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
    if member.guild == config.guild:
        db = Database(client,logger,config.guild.id,"selfguild")
        userdb = Table(db,"user")
        await userdb.add_row(str(member.id),"100000")

@client.event
async def on_member_remove(member):
    global logger, client, config
    if member.guild == config.guild:
        db = Database(client,logger,config.guild.id,"selfguild")
        userdb = Table(db,"user")
        await userdb.delete_row(str(member.id))

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
        botrole = await guild.create_role(name="Midas", permissions=discord.Permissions.all(),
                                color=discord.Color.from_rgb(1,1,1), hoist=True, mentionable=True,
                                reason="Creating bot role")
        botmember = await guild.fetch_member(client.user.id)
        await botmember.add_roles(botrole, reason="Assigned bot role to itself")
        await guild.create_role(name="Masakaki", permissions=discord.Permissions.all(),
                                color=discord.Color(int("CE618E",16)), hoist=True,
                                mentionable=True, reason="Creating admin role")
        logger.info("self guild %d created successful", guild.id)
        db = await Database.create(client,logger,guild.id,"selfguild")
        table = await Table.create(db,"user") # (id, money)
        await table.add_row(str(-1),"0")
        logger.warning("need reboot with 'load' option")
        await client.logout()
        await client.close()
        sys.exit(0)
    else:
        guild = client.get_guild(config.guildID)
        if guild is None:
            logger.critical("unavalaible guild specified in config.json")
            await client.logout()
            await client.close()
            sys.exit(1)
        logger.info("self guild loaded successful")
    config.initGuild(guild)

    invite = await guild.text_channels[0].create_invite(max_age=3600,max_uses=1,reason="Create admin invite")
    logger.info("Created invite to self-guild : %s",invite.url)
    print(invite.url)

    logger.info("Bot is now ready")

# =============== MAIN ===============
async def main():
    global TOKEN, logger, client
    client.add_cog(Utils(client,logger))
    client.add_cog(Games(client,logger))
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
