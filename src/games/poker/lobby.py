#!usr/bin/env python3.7
#-*-coding:utf-8-*-

import discord
from src.discord.database.database import *
from src.discord.database.table import *
from src.utils.config import *

class PokerLobby:
    def __init__(self,channel,minimalBet,bot,logger,round=10):
        self.minimalBet = minimalBe
        self.channel = channel
        config = Config()
        self.db = Database(bot,logger,config.guild.id,"selfguild")
        if not Table.exists(db,"poker"):
            Table.create(db,"poker")
        self.dbtable = Table(db,"poker")
        self.round = round
        self.player = []

    async def join(self,user):
        self.dbtable.add_row(str(self.channel.id),str(user.id),str(self.minimalBet))
        self.player.append(user)
        await self.channel.send("{} joined the table".format(str(user)))

    async def leave(self,user):
        self.dbtable.delete_row(str(self.channel.id),str(user.id))
        self.player.remove(user)
        await self.channel.send("{} left the table".format(str(user)))

    async def disband(self):
        self.dbtable.delete_row(str(self.channel.id))
        self.player = []
