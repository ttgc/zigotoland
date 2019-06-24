#!usr/bin/env python3.7
#-*-coding:utf-8-*-

import discord
from src.discord.database.exceptions import *
from src.discord.database.dataformat import *

class Table:
    def __init__(self,db,name):
        self.db = db
        self.name = name
        if not Table.exists(db, name):
            raise TableDoesNotExist(db, name)
        self.channel = discord.utils.get(db.category.text_channels, name=f"{db.name}-{name}")

    @staticmethod
    def exists(self,db,name):
        chan = discord.utils.get(db.category.text_channels, name=f"{db.name}-{name}")
        return chan is not None

    @classmethod
    async def create(cl,db,name):
        if cl.exists(db, name):
            raise TableAlreadyExist(db, name)
        await create_text_channel(f"{db.name}-{name}", reason="creating table in database")
        db.logger.info("Creating table %s in database %s",name,db.name)
        return cl(db, name)

    async def fetch(self):
        data = []
        self.db.logger.info("Fetching table %s from database %s ...",self.name,self.db.name)
        async for message in channel.history(limit=None):
            data.append(DataFormat.parse(message.content))
        self.db.logger.info("Fetching table %s from database %s finished",self.name,self.db.name)
        return data

    async def delete(self):
        await self.channel.delete(reason="delete table")
        self.db.logger.info("Removing table %s from database %s",self.name,self.db.name)

    async def add_row(self,*data):
        data = DataFormat(*data)
        await data.send(self.channel)
        self.db.logger.info("Added row to table %s from database %s",self.name,self.db.name)

    async def delete_row(self,identifier):
        #assume the identifier is always in the first column
        data = await self.fetch()
        async for message in channel.history(limit=None):
            data = DataFormat.parse(message.content)
            if data[0] == identifier:
                message.delete()
        self.db.logger.info("Removed row from table %s from database %s",self.name,self.db.name)
