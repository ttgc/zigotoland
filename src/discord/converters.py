#!usr/bin/env python3.7
#-*-coding:utf-8-*-

from discord.ext import commands

class RouletteConverter(commands.Converter):
    async def convert(self,ctx,arg):
        arg = arg.upper()
        if arg.startswith("R"):
            return "red", int(arg[1:])
        elif arg.startswith("B"):
            return "black", int(arg[1:])
        raise commands.ArgumentParsingError("unexisting area")
