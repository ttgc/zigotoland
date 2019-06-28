#!usr/bin/env python3.7
#-*-coding:utf-8-*-

import discord
from discord.ext import commands
from src.games.poker.lobby import *

class RouletteConverter(commands.Converter):
    async def convert(self,ctx,arg):
        arg = arg.upper()
        if arg.startswith("R"):
            return "red", int(arg[1:])
        elif arg.startswith("B"):
            return "black", int(arg[1:])
        raise commands.ArgumentParsingError("unexisting area")

class LobbyConverter(commands.Converter):
    async def convert(self,ctx,arg):
        cat = discord.utils.get(ctx.guild.categories, name="poker")
        chan = discord.utils.get(cat.text_channels, name=arg)
        lobby = PokerLobby.instances.get(chan, None)
        if lobby is None:
            raise commands.ArgumentParsingError("this poker lobby does not exists")
        return lobby
