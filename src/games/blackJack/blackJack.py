import math
import os
import random

deck = [1,2,3,4,5,6,7,8,9,10,'J','Q','K']*4
play_game = True

#bet = input("Make your bet")

def deal(deck):
    hand = []
    random.shuffle(deck)
    hand.append(deck[0])
    hand.append(deck[1])
    return hand

dealer_hand = deal(deck)
player_hand = deal(deck)

print(dealer_hand)
print(player_hand)


def calc_hand(hand):
    total = 0
    for i in range(len(hand)):
        if hand[i] == 'J' or hand[i] == 'Q' or hand[i] == 'K':
            total = total + 10
        else:
            total = total + int(hand[i])
    return total

print(calc_hand(dealer_hand))
print(calc_hand(player_hand))

def blackjack(dealer_hand, player_hand):
    if calc_hand(dealer_hand)==21:
       print("loser")
    elif calc_hand(player_hand)==21:
        print("winner")
    elif calc_hand(player_hand) < calc_hand(dealer_hand):
        print("loser")
    elif calc_hand(player_hand) > calc_hand(dealer_hand):
        print("winner")


blackjack(dealer_hand, player_hand)


def result(dealer_hand, player_hand):
    print("player: " + player_hand)
    print("dealer: " + dealer_hand)
