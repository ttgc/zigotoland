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
            if x = random.randint(1,100) < 3:
                list.append(i)
            elif x = random.randint(1,100) < 3:
                list.append(i)
            elif x = random.randint(1,100) < 3:
                list.append(i)
            else:
                list.append(i)
        return list


    #Random draws for the pennyMachine
    first_draw = choice(list)
    second_draw = choice(list)
    third_draw = choice(list)


    #winning conditions

    if first_draw == second_draw and second_draw == third_draw:
        pass
        
