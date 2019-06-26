import random
import os
import logging
import asyncio


tokens = 5000
money_up1 = 0.5
money_up2 = 1
money_up3 = 2
money_up4 = 4
money_up5 = 10
money_up6 = 100
money_up7 = 1000
money_down1 = -0.7
money_down2 = -0.6
money_down3 = -0.5
money_down4 = -0.4
money_down5 = -0.3
money_down6 = -0.2
money_down7 = -0.1
full_lose = -1


    async def pennymachine():
        #select the amount of tokens to bet
        bet = 0
        logging.info("Choisir la mise")
        bet = input("Make your bet: ")

        try:
            bet = int(bet)
        except:
            logging.log(logger.DEBUG+1, "Cant cast bet to int")
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
        list = fake_randomiser()


        #Random draws for the pennyMachine
        def draws():
            for i in range(3):
                if i == 1:
                    await bot.send_message(emojize(":poop: :poop: :poop:", use_aliases = True))
                elif i == 2:
                    await bot.send_message(emojize(":monkey_face: :monkey_face: :monkey_face:", use_aliases = True))
                elif i == 3:
                    await bot.send_message(emojize(":watermelon: :watermelon: :watermelon:", use_aliases = True))
                elif i == 4:
                    await bot.send_message(emojize(":banana: :banana: :banana:", use_aliases = True))
                elif i == 5:
                    await bot.send_message(emojize(":kiwi: :kiwi: :kiwi:", use_aliases = True))
                elif i == 6:
                    await bot.send_message(emojize(":monkey_face: :monkey_face: :monkey_face:", use_aliases = True))
                else i == 7:
                    await bot.send_message(emojize(":moneybag: :moneybag: :moneybag:", use_aliases = True))

        #winning conditions
        if first_draw == second_draw and second_draw == third_draw:
            if first_draw == 7:
                logging.log(logging.DEBUG+1,"Finally...")
                tokens = tokens + bet * money_up7
            elif first_draw == 6:
                logging.log(logging.DEBUG+1,"You lucker...")
                tokens = tokens + bet * money_up6
            elif first_draw == 5:
                logging.log(logging.DEBUG+1,"Is that all you've got?")
                tokens = tokens + bet * money_up5
            elif first_draw == 4:
                logging.log(logging.DEBUG+1,"Meh...")
                tokens = tokens + bet * money_up4
            elif first_draw == 3:
                logging.log(logging.DEBUG+1,"LUL")
                tokens = tokens + bet * money_up3
            elif first_draw == 2:
                logging.log(logging.DEBUG+1,"you loser!")
                tokens = tokens + bet * money_up2
            elif first_draw == 1:
                logging.log(logging.DEBUG+1,"traaash")
                tokens = tokens + bet * money_up1
        elif first_draw == second_draw or first_draw == third_draw or second_draw == third_draw:
            if first_draw == 7:
                logging.log(logging.DEBUG+1,"Finally...")
                tokens = tokens + bet * money_down7
            elif first_draw == 6:
                logging.log(logging.DEBUG+1,"You lucker...")
                tokens = tokens + bet * money_down6
            elif first_draw == 5:
                logging.log(logging.DEBUG+1,"Is that all you've got?")
                tokens = tokens + bet * money_down5
            elif first_draw == 4:
                logging.log(logging.DEBUG+1,"Meh...")
                tokens = tokens + bet * money_down4
            elif first_draw == 3:
                logging.log(logging.DEBUG+1,"LUL")
                tokens = tokens + bet * money_down3
            elif first_draw == 2:
                logging.log(logging.DEBUG+1,"you loser!")
                tokens = tokens + bet * money_down2
            elif first_draw == 1:
                logging.log(logging.DEBUG+1,"traaash")
                tokens = tokens + bet * money_down1
            else:
                tokens = tokens + bet * full_lose
        print(tokens)

        if tokens <= 0:
            logging.info("player broke, ban him!")
