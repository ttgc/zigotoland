#!usr/bin/env python3.7
#-*-coding:utf-8-*-

import discord
from discord.ext import commands
from src.discord.checks import *
from src.discord.database.database import *
from src.discord.database.table import *
from src.discord.manage import *
import logging
import math

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

    @commands.check(check_inserv)
    @commands.command()
    async def economy(self,ctx):
        """Show the current financial indicator of the financial district.
        This indicator may lower money earned in the whole financial district.
        It evolves only if darkness members use the rotary press"""
        db = Database(self.bot,self.logger,ctx.guild.id,"selfguild")
        usertable = Table(db,"user")
        userlist = await usertable.fetch()
        for servdb in userlist:
            if "-1" == servdb[0]: break
        if int(servdb[1]) < 0:
            color = discord.Color(int("FF0000",16))
        else:
            color = discord.Color(int("00FF00",16))
        embd = discord.Embed(title="Current economy indicator of the financial district",description="Financial district information",colour=color)
        embd.set_footer(text="Bot created by Ttgc and Trakozz",icon_url=self.bot.user.avatar_url)
        embd.set_author(name=str(ctx.author),icon_url=ctx.author.avatar_url)
        embd.add_field(name="Economy indicator :", value=int(servdb[1]), inline=True)

        await ctx.channel.send(embed=embd)

    @commands.check(check_darkmember)
    @commands.group(invoke_without_command=False)
    async def rotarypress(self,ctx): pass

    @rotarypress.command(name="rotate")
    async def rotarypress_rotate(self,ctx,amount: int):
        """Reserved to darkness members.
        Make rotating the rotary press, printing money and distributing the same amount to all accounts.
        In exchange of producing money, this will reduce proportionnally the global financial indicator of the district, reducing money earned in the future"""
        amount = abs(amount)
        if amount < 1000:
            await ctx.channel.send("You should at least print 1000 dollars for each account")
            return
        fallindicator = round(amount/100)
        db = Database(self.bot,self.logger,ctx.guild.id,"selfguild")
        usertable = Table(db,"user")
        userlist = await usertable.fetch()
        for user in userlist:
            if user[0] == "-1":
                await usertable.update_row(user[0], str(int(user[1]) - fallindicator))
            else:
                await usertable.update_row(user[0], str(int(user[1]) + amount))
        self.logger.info("Rotary press activated by %d to print %d dollars",ctx.author.id,amount)
        await ctx.channel.send("{} The rotary press has been activated by {} to print {} dollars for each account".format(ctx.guild.default_role.mention,ctx.author.mention,amount))

    @rotarypress.command(name="getmoney")
    async def rotarypress_reverse(self,ctx,amount: int):
        """Reserved to darkness members.
        Reverse rotation of the rotary press, printed money from the rotary press is taken back from accounts
        In exchange, this will increase proportionnally the global financial indicator of the district, increasing money earned in the future"""
        amount = abs(amount)
        if amount < 1000:
            await ctx.channel.send("You should at least take back 1000 dollars for each account")
            return
        raiseindicator = round(amount/100)
        db = Database(self.bot,self.logger,ctx.guild.id,"selfguild")
        usertable = Table(db,"user")
        userlist = await usertable.fetch()
        for srv in userlist:
            if srv[0] == -1: break
        if int(srv[1]) + raiseindicator > 0:
            await ctx.channel.send("You cannot return more money than previously printed by the rotary press")
            return
        for user in userlist:
            if user[0] == "-1":
                await usertable.update_row(user[0], str(int(user[1]) + raiseindicator))
            else:
                await usertable.update_row(user[0], str(int(user[1]) - amount))
        self.logger.info("Rotary press reverse by %d to return %d dollars",ctx.author.id,amount)
        await ctx.channel.send("{} The rotary press has been reversed by {} to return {} dollars".format(ctx.guild.default_role.mention,ctx.author.mention,amount))
