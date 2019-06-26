#!usr/bin/env python3.7
#-*-coding:utf-8-*-

import discord
from src.discord.database.database import *
from src.discord.database.table import *
from src.utils.config import *

class PokerLobby:
    instances = {}
    config = Config()

    def __init__(self,owner,channel,minimalBet,bot,logger,round=10):
        self.minimalBet = minimalBet
        self.channel = channel
        self.db = Database(bot,logger,PokerLobby.config.guild.id,"selfguild")
        self.usertable = Table(self.db,"user")
        self.round = round
        self.player = {}
        self.perms = discord.PermissionOverwrite()
        self.perms.send_messages = True
        self.perms.read_messages = True
        self.logger = logger
        self.logger.info("creating lobby for poker : %s", str(self.channel))
        self.owner = owner
        PokerLobby.instances[self.channel] = self

    async def join(self,user):
        self.player[user] = self.minimalBet
        await self.channel.send("{} joined the table".format(str(user)))
        await self.channel.set_permissions(user, overwrite=self.perms, reason="joining poker lobby")
        self.logger.info("user %d joining poker lobby %s", user.id, str(self.channel))

    async def leave(self,user):
        usrlist = await self.usertable.fetch()
        for usr in usrlist:
            if usr[0] == str(user.id): break
        moneyEarned = self.player[user] - self.minimalBet
        self.usertable.update_row(str(user.id), str(int(usr[1]) + moneyEarned))
        del(self.player[user])
        await self.channel.send("{} left the table".format(str(user)))
        await self.channel.set_permissions(user, overwrite=None, reason="leaving poker lobby")
        self.logger.info("user %d leaving poker lobby %s", user.id, str(self.channel))

    async def disband(self):
        for usr in self.player.keys():
            await self.leave(usr)
        del(PokerLobby.instances[self.channel])
        self.logger.info("disband poker lobby %s", str(self.channel))
        await self.channel.delete(reason="disband poker lobby")
