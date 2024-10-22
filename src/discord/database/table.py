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
        self.channel = discord.utils.get(db.category.text_channels, name="{}-{}".format(db.name,name))

    @staticmethod
    def exists(db,name):
        chan = discord.utils.get(db.category.text_channels, name="{}-{}".format(db.name,name))
        return chan is not None

    @classmethod
    async def create(cl,db,name):
        if cl.exists(db, name):
            raise TableAlreadyExist(db, name)
        await db.category.create_text_channel("{}-{}".format(db.name,name), reason="creating table in database")
        db.logger.info("Creating table %s in database %s",name,db.name)
        return cl(db, name)

    async def fetch(self):
        data = []
        self.db.logger.info("Fetching table %s from database %s ...",self.name,self.db.name)
        async for message in self.channel.history(limit=None):
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
        async for message in self.channel.history(limit=None):
            data = DataFormat.parse(message.content)
            if data[0] == identifier:
                await message.delete()
        self.db.logger.info("Removed row from table %s from database %s",self.name,self.db.name)

    async def update_row(self,identifier,*data):
        #assume the identifier is always in the first column
        data = DataFormat(identifier,*data)
        async for message in self.channel.history(limit=None):
            datadb = DataFormat.parse(message.content)
            if datadb[0] == identifier:
                await message.edit(content=str(data))
        self.db.logger.info("Updated row from table %s from database %s",self.name,self.db.name)
