from random import *
from math import *
import logger

tokens = 5000
play_game = True

while play_game:

    #select the amount of tokens to bet
    bet = 0
    logger.info("Choisir la mise")
    bet = input("Make your bet")
    if bet > 0 and bet < tokens:
        try:
            bet = int(bet)
        except:
            logger.log(logger.DEBUG+1, "Cant cast bet to int")
        finally:
            pass

    #Fake Randomiser
    def fake_randomiser():
        list=[]
        for i in range(100):
            x = random.randint(1,100)
            if x <= 1:
                list.append(7)
            elif x <= 5:
                list.append(6)
            elif x <= 12:
                list.append(5)
            elif x <= 20:
                list.append(4)
            elif x <= 35:
                list.append(3)
            elif x <= 65:
                list.append(2)
            else:
                list.append(1)
        return list


    #Random draws for the pennyMachine
    first_draw = choice(list)
    second_draw = choice(list)
    third_draw = choice(list)


    #winning conditions

    if first_draw == second_draw and second_draw == third_draw:
        if first_draw == 7:
            logger.info("JACKPOT!!!")
        elif first_draw == 6:
            logger.info("Pas trop mal")
        elif first_draw == 5:
            logger.info("Peut mieux faire")
        elif first_draw == 4:
            logger.info("Bof")
        elif first_draw == 3:
            logger.info("LUL")
        elif first_draw == 2:
            logger.info("you loser!")
        elif first_draw == 1:
            logger.info("traaash")
