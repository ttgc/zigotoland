#!usr/bin/env python3.7
#-*-coding:utf-8-*-

import discord
from discord.ext import commands
from src.discord.checks import *
from src.discord.database.database import *
from src.discord.database.table import *
from src.discord.manage import *
import logging

class Economy(commands.Cog):
    def __init__(self,bot,logger):
        self.bot = bot
        self.logger = logger

    @commands.check(check_inserv)
    @commands.command(aliases=["money", "coins"])
    async def wallet(self,ctx):
        gold, plat, dark = await manage_roles(ctx, self.logger)
        db = Database(self.bot,self.logger,ctx.guild.id,"selfguild")
        usertable = Table(db,"user")
        userlist = await usertable.fetch()
        for user in userlist:
            if str(ctx.author.id) == user[0]: break

        money = int(user[1])
        if dark in ctx.author.roles:
            color = dark.color
            card = "https://vignette.wikia.nocookie.net/soulcontrol/images/5/50/Mikuni_card.jpg/revision/latest?cb=20110508191230"
        elif plat in ctx.author.roles:
            color = plat.color
            card = "https://vignette.wikia.nocookie.net/soulcontrol/images/d/d5/Kou_card.jpg/revision/latest?cb=20110508191202"
        elif gold in ctx.author.roles:
            color = gold.color
            card = "https://vignette.wikia.nocookie.net/soulcontrol/images/e/ee/Jenny_card.jpg/revision/latest?cb=20110508191130"
        else:
            color = discord.Color(int("FF0000",16))
            card = "https://vignette.wikia.nocookie.net/soulcontrol/images/f/f9/Kimi_card.jpg/revision/latest?cb=20110508191032"

        embd = discord.Embed(title="Current wallet",description="Financial district bank account information",colour=color)
        embd.set_footer(text="Bot created by Ttgc and Trakozz",icon_url=self.bot.user.avatar_url)
        embd.set_thumbnail(url=card)
        embd.set_author(name=str(ctx.author),icon_url=ctx.author.avatar_url)
        embd.add_field(name="Currently on your account :", value="{} dollars".format(money), inline=True)

        await ctx.channel.send(embed=embd)

    @commands.check(check_inserv)
    @commands.command(aliases=["give"])
    async def transfer(self,ctx,amount: int,target: discord.Member):
        amount = abs(amount)
        db = Database(self.bot,self.logger,ctx.guild.id,"selfguild")
        usertable = Table(db,"user")
        userlist = await usertable.fetch()
        for usersrc in userlist:
            if str(ctx.author.id) == usersrc[0]: break
        for usertarget in userlist:
            if str(target.id) == usertarget[0]: break
        await usertable.update_row(usersrc[0], str(int(usersrc[1]) - amount))
        await usertable.update_row(usertarget[0], str(int(usertarget[1]) + amount))
        await ctx.channel.send("{} have transfered {} dollars to {} account".format(ctx.author.mention, amount, target.mention))
