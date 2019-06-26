#!usr/bin/env python3.7
#-*-coding:utf-8-*-

import discord
from src.games.poker.cardset import *
from src.games.poker.lobby import *

class PokerRound:
    def __init__(self,lobby):
        self.lobby = lobby
        self.curbet = {}
        self.cards = {}
        self.playerlist = []
        self.totalbet = 100*len(lobby.player)
        for i in lobby.player.keys():
            self.curbet[i] = 100
            lobby.player[i] -= 100
            self.cards[i] = CardSet.give(2)
            self.playerlist.append(i)
        self.flop = CardSet.give(3)
        self.turn = CardSet.give(1)
        self.river = CardSet.give(1)
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
        return self.playing, changeTour

    def fold(self,player):
        self.lobby.player[player] -= self.curbet[player]
        del(self.curbet[player])
        del(self.cards[player])
        self.playerlist.remove(player)
        return self.nextplayer()

    def follow(self,player):
        self.curbet[player] = self.curbet[self.playerlist[self.indexplaying-1]]
        self.totalbet = 0
        for i in self.curbet.values():
            self.totalbet += i
        return self.nextplayer()

    def raise_(self,player,amount):
        self.curbet[player] += amount
        self.totalbet = 0
        for i in self.curbet.values():
            self.totalbet += i
        return self.nextplayer()

    async def endturn(self):
        if self.tour == 2:
            return self.flop
        if self.tour == 3:
            return self.turn
        if self.tour == 4:
            return self.river
        if self.tour == 5:
            end = await self.endgame()
            return end

    async def endgame(self):
        winner = None
        winnerCard = []
        for i in self.lobby.player.keys():
            self.lobby.player[i] -= self.curbet[i]
            if winner is None or (CardSet.compare(winnerCard, self.cards[i]) == 1 and i != winner):
                winner = i
                winnerCard = self.cards[i]
        self.lobby.player[winner] += self.totalbet
        clearlist = []
        for i,k in self.lobby.player.items():
            if k <= 0:
                await self.lobby.leave(i,False)
                clearlist.append(i)
        for i in clearlist: del(self.lobby.player[i])
        self.lobby.curround = None
        return winner
