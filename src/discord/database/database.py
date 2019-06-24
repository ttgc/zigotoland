#!usr/bin/env python3.7
#-*-coding:utf-8-*-

import discord
from src.discord.database.exceptions import *

class Database:
    def __init__(self,bot,logger,servid,name):
        self.bot = bot
        self.logger = logger
        self.srv = discord.utils.get(self.bot.guilds, id=servid)
        if self.srv is None:
            raise ServerNotFoundException(servid)
        self.category = discord.utils.get(self.srv.categories, name=f"python.db={name}")
        if self.category is None:
            raise DatabaseDoesNotExist(name)

    @staticmethod
    def exists(bot,servid,name):
        srv = discord.utils.get(bot.guilds, id=servid)
        if srv is None: return False
        category = discord.utils.get(srv.categories, name=f"python.db={name}")
        return category is not None

    @classmethod
    async def create(cl,bot,logger,servid,name):
        if cl.exists(servid, name):
            raise DatabaseAlreadyExist(name)
        srv = discord.utils.get(bot.guilds, id=servid)
        if self.srv is None:
            raise ServerNotFoundException(servid)
        botperm = discord.PermissionOverwrite(read_messages=True, send_messages=True,
                    manage_messages=True,
                    read_message_history=True)
        everyoneperm = discord.PermissionOverwrite(read_messages=False, send_messages=False,
                    manage_messages=False,
                    read_message_history=False)
        perms = {self.bot.user: botperm, srv.default_role: everyoneperm}
        await srv.create_category_channel(f"python.db={name}", overwrites=perms, reason="database create")
        logger.info("Create database in center %s named %s",str(srv),name)
        return cl(bot,logger,servid,name)
