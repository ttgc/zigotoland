import typing
import discord
import logging
import asyncio
import emojis
from discord.ext import commands
from src.games.pennyMachine.pennyMachine import *
client = discord.Client()

class PennyMachineCog(commands.Cog):

    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger

    #@commands.check()
    @commands.command()
    async def pennyMachine(self, ctx, bet):
        pass

    @client.event
    async def on_message(message):
        author = message.author

    @commands.command()
    async pennymachine(self, ctx, bet: int):
        """Make your bet and pray for the win"""

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

        db = Database(self.bot,self.logger,ctx.guild.id,"selfguild")
        usertable = Table(db,"user")
        users = await usertable.fetch()
        for user in users:
            if user[0] == str(ctx.author.id): break
        coins = int(user[1]) - bet

        draw1, draw2, draw3 = 0, 0, 0
        list = [randint(1, 100), randint(1, 100), randint(1, 100)]
        for i in range(3):
            if i < 3: draw+"i" = 7
            elif i < 8: draw+"i" = 6
            elif i < 15: draw+"i" = 5
            elif i < 25: draw+"i" = 4
            elif i < 40: draw+"i" = 3
            elif i < 65: draw+"i" = 2
            elif i < 20: draw+"i" = 1

        for i in range(3):
            await asyncio.sleep(0.2)
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


        if first_draw == second_draw and second_draw == third_draw:
            if first_draw == 7:
                await ctx.channel.send("You win ! you have earned : {} coins".format(bet*money_up7))
                coins += (bet*money_up7)
            elif first_draw == 6:
                await ctx.channel.send("You win ! you have earned : {} coins".format(bet*money_up6))
                coins += (bet*money_up6)
            elif first_draw == 5:
                await ctx.channel.send("You win ! you have earned : {} coins".format(bet*money_up5))
                coins += (bet*money_up5)
            elif first_draw == 4:
                await ctx.channel.send("You win ! you have earned : {} coins".format(bet*money_up4))
                coins += (bet*money_up4)
            elif first_draw == 3:
                await ctx.channel.send("You win ! you have earned : {} coins".format(bet*money_up3))
                coins += (bet*money_up3)
            elif first_draw == 2:
                await ctx.channel.send("You win ! you have earned : {} coins".format(bet*money_up2))
                coins += (bet*money_up2)
            elif first_draw == 1:
                await ctx.channel.send("You win ! you have earned : {} coins".format(bet*money_up1))
                coins += (bet*money_up1)
        elif first_draw == second_draw or first_draw == third_draw or second_draw == third_draw:
            if first_draw == 7:
                await ctx.channel.send("You win ! you have lost : {} coins".format(bet*money_down7))
                coins += (bet*money_down5)
            elif first_draw == 6:
                await ctx.channel.send("You win ! you have lost : {} coins".format(bet*money_down6))
                coins += (bet*money_down5)
            elif first_draw == 5:
                await ctx.channel.send("You win ! you have lost : {} coins".format(bet*money_down5))
                coins += (bet*money_down5)
            elif first_draw == 4:
                await ctx.channel.send("You win ! you have lost : {} coins".format(bet*money_down4))
                coins += (bet*money_down4)
            elif first_draw == 3:
                await ctx.channel.send("You win ! you have lost : {} coins".format(bet*money_down3))
                coins += (bet*money_down3)
            elif first_draw == 2:
                await ctx.channel.send("You win ! you have lost : {} coins".format(bet*money_down2))
                coins += (bet*money_down2)
            elif first_draw == 1:
                await ctx.channel.send("You win ! you have lost : {} coins".format(bet*money_down1))
                coins += (bet*money_down1)
        else:
            await ctx.channel.send("You lose ! you have lost : {} coins".format(bet*full_lose))
            coins += (bet*full_lose)

        await usertable.update_row(user[0],str(coins))
