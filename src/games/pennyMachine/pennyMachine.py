from random import *
from math import *
import logger

play_game = True
tokens = 5000
money1 = 0.5
money2 = 1
money3 = 2
money4 = 4
money5 = 10
money6 = 100
money7 = 1000

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
            elif x <= 50:
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
            logger.log(logger.DEBUG+1,"Finally...")
            tokens = tokens + bet * money7
        elif first_draw == 6:
            logger.log(logger.DEBUG+1,"You lucker...")
            tokens = tokens + bet * money6
        elif first_draw == 5:
            logger.log(logger.DEBUG+1,"Is that all you've got?")
            tokens = tokens + bet * money5
        elif first_draw == 4:
            logger.log(logger.DEBUG+1,"Meh...")
            tokens = tokens + bet * money4
        elif first_draw == 3:
            logger.log(logger.DEBUG+1,"LUL")
            tokens = tokens + bet * money3
        elif first_draw == 2:
            logger.log(logger.DEBUG+1,"you loser!")
            tokens = tokens + bet * money2
        elif first_draw == 1:
            logger.log(logger.DEBUG+1,"traaash")
            tokens = tokens + bet * money1

    if tokens <= 0:
        logger.info("player broke, ban him!")
        
