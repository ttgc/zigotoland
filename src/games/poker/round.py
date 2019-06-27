#!usr/bin/env python3.7
#-*-coding:utf-8-*-

import discord
import asyncio
from src.games.poker.cardset import *
from src.games.poker.lobby import *

class PokerRound:
    def __init__(self,lobby):
        self.lobby = lobby
        self.curbet = {}
        self.cards = {}
        self.playerlist = []
        self.cardset = CardSet()
        self.totalbet = 100*len(lobby.player)
        for i in lobby.player.keys():
            self.curbet[i] = 100
            lobby.player[i] -= 100
            self.cards[i] = self.cardset.give(2)
            self.playerlist.append(i)
        self.flop = self.cardset.give(3)
        self.turn = self.cardset.give(1)
        self.river = self.cardset.give(1)
        self.playing = self.playerlist[0]
        self.indexplaying = 0
        self.tour = 1

    def nextplayer(self):
        self.indexplaying += 1
        changeTour = False
        if self.indexplaying >= len(self.playerlist):
            self.indexplaying = 0
            self.tour += 1
            changeTour = True
        self.playing = self.playerlist[self.indexplaying]
        return changeTour

    async def check_remains_player(self):
        if len(self.playerlist) <= 1:
            await self.endgame()
            return False
        return True

    async def fold(self,player):
        self.lobby.player[player] -= self.curbet[player]
        del(self.curbet[player])
        del(self.cards[player])
        self.playerlist.remove(player)
        await self.lobby.channel.send("{} is folding".format(player.mention))
        return self.nextplayer()

    async def follow(self,player):
        self.curbet[player] = self.curbet[self.playerlist[self.indexplaying-1]]
        self.totalbet = 0
        for i in self.curbet.values():
            self.totalbet += i
        await self.lobby.channel.send("{} is following".format(player.mention))
        return self.nextplayer()

    async def raise_(self,player,amount):
        self.curbet[player] = self.curbet[self.playerlist[self.indexplaying-1]]
        self.curbet[player] += amount
        self.totalbet = 0
        for i in self.curbet.values():
            self.totalbet += i
        await self.lobby.channel.send("{} is raising the bet with {} more coins".format(player.mention, amount))
        return self.nextplayer()

    async def inform_player(self, supset=[]):
        for i,k in self.cards.items():
            combi = CardSet.combination[CardSet.retrieveCombination(k+supset)]
            cardlist = ""
            for card in k+supset:
                cardlist += "{}\n".format(card)
            await i.send("Your current hand combination is : {}\n```\n{}\n```".format(combi, cardlist))
            await asyncio.sleep(0.2)

    async def endturn(self):
        if self.tour == 2:
            await self.inform_player(self.flop)
            await self.lobby.channel.send("End of turn 1 : The flop is :\n```\n{}\n{}\n{}\n```".format(self.flop[0],self.flop[1],self.flop[2]))
            return self.flop
        elif self.tour == 3:
            await self.inform_player(self.flop + self.turn)
            await self.lobby.channel.send("End of turn 2 : The turn is : `{}`".format(self.turn[0]))
            return self.turn
        elif self.tour == 4:
            await self.inform_player(self.flop + self.turn + self.river)
            await self.lobby.channel.send("End of turn 3 : The river is : `{}`".format(self.river[0]))
            return self.river
        elif self.tour == 5:
            await self.inform_player(self.flop + self.turn + self.river)
            end = await self.endgame()
            return end

    async def endgame(self):
        winner = None
        winnerCard = []
        for i in self.playerlist:
            self.lobby.player[i] -= self.curbet[i]
            cards = self.cards[i]+self.flop+self.turn+self.river
            if winner is None or (CardSet.deepcompare(winnerCard, cards) > 0 and i != winner):
                winner = i
                winnerCard = cards
            await self.lobby.channel.send("Player {} has the following cards : `{}` and `{}`".format(i.mention, self.cards[i][0], self.cards[i][1]))
        self.lobby.player[winner] += self.totalbet
        clearlist = []
        self.lobby.curround = None
        for i,k in self.lobby.player.items():
            if k <= 0:
                await self.lobby.leave(i,False)
                clearlist.append(i)
        await self.lobby.channel.send("End of the round !\nThe winner is {} with {} and earned {} coins".format(winner.mention, CardSet.combination[CardSet.retrieveCombination(winnerCard)], self.totalbet))
        await asyncio.sleep(1)
        for i in clearlist: del(self.lobby.player[i])
        return winner
