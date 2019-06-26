#!usr/bin/env python3.7
#-*-coding:utf-8-*-

import discord
from src.discord.database.database import *
from src.discord.database.table import *
from src.utils.config import *

class PokerLobby:
    instances = {}

    def __new__(cl,channel,minimalBet,bot,logger,round=10):
        return instances.get(channel, Object.__new__(cl,channel,minimalBet,bot,logger,round))

    def __init__(self,channel,minimalBet,bot,logger,round=10):
        self.minimalBet = minimalBet
        self.channel = channel
        config = Config()
        self.db = Database(bot,logger,config.guild.id,"selfguild")
        self.usertable = Table(db,"user")
        self.round = round
        self.player = {}

    async def join(self,user):
        self.player[user] = self.minimalBet
        await self.channel.send("{} joined the table".format(str(user)))

    async def leave(self,user):
        usrlist = await self.usertable.fetch()
        for usr in usrlist:
            if usr[0] == str(user.id)
        moneyEarned = self.player[user] - self.minimalBet
        self.usertable.update_row(str(user.id), str(int(usr[1]) + moneyEarned))
        del(self.player[user])
        await self.channel.send("{} left the table".format(str(user)))

    async def disband(self):
        for usr in self.player.keys():
            await self.leave(usr)
        del(PokerLobby.instances[self.channel])
