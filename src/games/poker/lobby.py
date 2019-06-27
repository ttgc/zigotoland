#!usr/bin/env python3.7
#-*-coding:utf-8-*-

import discord
from src.discord.database.database import *
from src.discord.database.table import *
from src.utils.config import *
from src.games.poker.round import *

class PokerLobby:
    instances = {}
    config = Config()

    def __init__(self,owner,channel,minimalBet,bot,logger,round_=10):
        self.minimalBet = minimalBet
        self.channel = channel
        self.db = Database(bot,logger,PokerLobby.config.guild.id,"selfguild")
        self.usertable = Table(self.db,"user")
        self.round = round_
        self.player = {}
        self.perms = discord.PermissionOverwrite()
        self.perms.send_messages = True
        self.perms.read_messages = True
        self.logger = logger
        self.logger.info("creating lobby for poker : %s", str(self.channel))
        self.owner = owner
        self.curround = None
        self.curnbrround = 0
        PokerLobby.instances[self.channel] = self

    async def join(self,user):
        self.player[user] = self.minimalBet
        await self.channel.send("{} joined the table".format(user.mention))
        await self.channel.set_permissions(user, overwrite=self.perms, reason="joining poker lobby")
        self.logger.info("user %d joining poker lobby %s", user.id, str(self.channel))

    async def leave(self,user,delete=True):
        if self.curround is not None:
            await self.curround.fold(user)
        usrlist = await self.usertable.fetch()
        for usr in usrlist:
            if usr[0] == str(user.id): break
        moneyEarned = self.player[user] - self.minimalBet
        await self.usertable.update_row(str(user.id), str(int(usr[1]) + moneyEarned))
        if delete: del(self.player[user])
        await self.channel.send("{} left the table".format(user.mention))
        await self.channel.set_permissions(user, overwrite=None, reason="leaving poker lobby")
        self.logger.info("user %d leaving poker lobby %s", user.id, str(self.channel))

    async def disband(self):
        for usr in self.player.keys():
            await self.leave(usr, False)
        self.player = {}
        del(PokerLobby.instances[self.channel])
        self.logger.info("disband poker lobby %s", str(self.channel))
        await self.channel.delete(reason="disband poker lobby")

    async def check_auto_disband(self):
        if self.curnbrround == self.round and self.curround is None:
            await self.disband()

    def startround(self):
        if self.curnbrround < self.round:
            self.curnbrround += 1
            self.curround = PokerRound(self)
            return self.curround
