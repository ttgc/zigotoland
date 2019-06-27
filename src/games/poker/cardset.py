#!usr/bin/env python3.7
#-*-coding:utf-8-*-

from random import shuffle

class CardSet:
    color = ["Spade", "Club", "Diamond", "Spades"]
    value = ["7","8","9","10","Jack","Queen","King","As"]
    combination = ["none","pair","double pair","brelan","quinte","color","full","square","quinte flush","royal quinte flush"]

    def __init__(self):
        self.cards = []
        for i in range(len(CardSet.color)):
            for k in range(len(CardSet.value)):
                self.cards.append(CardSet.formatCard(k, i))
        shuffle(self.cards)

    def give(self,number):
        ls = []
        for i in range(number):
            ls.append(self.cards.pop(0))
        return ls

    @classmethod
    def compare(cl, set1, set2):
        return retrieveCombination(set2) - retrieveCombination(set1)

    @classmethod
    def sortFlush(cl, set):
        cpy = set[:]
        cpy.sort(key=Card.truevalue)
        return cpy

    @classmethod
    def sortValue(cl, set):
        cpy = set[:]
        cpy.sort(key=lambda card: card.value)
        return cpy

    @classmethod
    def retrieveCombination(cl, set):
        combi = 0
        samenumber = [0 for i in range(len(cl.value))]
        samecolor = [0 for i in range(len(cl.color))]
        numberoccur = [0 for i in range(8)]
        coloroccur = [0 for i in range(8)]

        for card in set:
            samenumber[card.value] += 1
            samecolor[card.color] += 1
        for i in samenumber:
            numberoccur[i] += 1
            coloroccur[i] += 1
        quinte = False
        if (numberoccur[1] >= 5):
            ordered = cl.sortValue(set)
            maximal = 0
            current = 0
            for i in range(1,len(ordered)):
                if ordered[i].value == ordered[i-1].value - 1:
                    current += 1
                else:
                    if current > maximal: maximal = current
                    current = 0
            quinte = maximal >= 5
        color = (coloroccur[5] == 1 or coloroccur[6] == 1 or coloroccur[7] == 1)
        quinte_flush = False
        if (quinte and color):
            ordered = cl.sortFlush(set)
            maximal = 0
            current = 0
            for i in range(1,len(ordered)):
                if ordered[i].value == ordered[i-1].value - 1 and ordered[i].color == ordered[i-1].color:
                    current += 1
                else:
                    if current > maximal: maximal = current
                    current = 0
            quinte_flush = maximal >= 5
        royal = quinte_flush and samenumber[-1] == 1 and samenumber[-2] == 1 and samenumber[-3] == 1 and samenumber[-4] == 1 and samenumber[-5] == 1

        if royal: return 9
        if quinte_flush: return 8
        if 4 in samenumber: return 7
        if 3 in samenumber and 2 in samenumber: return 6
        if color: return 5
        if quinte: return 4
        if 3 in samenumber: return 3
        if numberoccur[2] == 2: return 2
        if 2 in samenumber: return 1
        return 0

class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __str__(self):
        return "{} of {}".format(CardSet.value[self.value], CardSet.color[self.color])

    @classmethod
    def truevalue(cl, card):
        return (self.color*100)+self.value
