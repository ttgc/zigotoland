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


    # cherries = self.bot.emojis.find(emoji => emoji.name === "cherries");
    # banana = self.bot.emojis.find(emoji => emoji.name === "banana");
    # kiwi = self.bot.emojis.find(emoji => emoji.name === "kiwi");
    # watermelon = self.bot.emojis.find(emoji => emoji.name === "watermelon");
    # moneybag = self.bot.emojis.find(emoji => emoji.name === "moneybag");
    # poop = self.bot.emojis.find(emoji => emoji.name === "poop");
    # monkey_face = self.bot.emojis.find(emoji => emoji.name === "monkey_face");


    #@commands.check()
    @commands.command()
    async def pennyMachine(self, ctx, bet):
        pass

    @client.event
    async def on_message(message):
        author = message.author

    @commands.command()
    async def start_game(self, ctx, *, member: discord.Member = None):
        await bot.send_message(emojize(":poop: :poop: :poop:", use_aliases = True))
        await bot.send_message(emojize(":poop: :poop: :poop:", use_aliases = True))
        await bot.send_message(emojize(":poop: :poop: :poop:", use_aliases = True))
        await bot.send_message(emojize(":poop: :poop: :poop:", use_aliases = True))
        await bot.send_message(emojize(":poop: :poop: :poop:", use_aliases = True))
        await bot.send_message(emojize(":poop: :poop: :poop:", use_aliases = True))
        await bot.send_message(emojize(":poop: :poop: :poop:", use_aliases = True))
