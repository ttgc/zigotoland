#!usr/bin/env python3.7
#-*-coding:utf-8-*-

from discord.ext import commands
from src.discord.checks import *
import logging, sys

class Utils(commands.Cog):
    def __init__(self,bot,logger):
        self.bot = bot
        self.logger = logger

    @commands.check(check_botowner)
    @commands.command(aliases=["eval"])
    async def debug(self,ctx,*,arg):
        self.logger.log(logging.DEBUG+1,"running debug instruction : %s",arg.replace("```python","").replace("```",""))
        exec(arg.replace("```python","").replace("```",""))

    @commands.check(check_botowner)
    @commands.command()
    async def invite(self,ctx):
        botaskperm = discord.Permissions().all()
        botaskperm.administrator = botaskperm.manage_channels = botaskperm.manage_guild = botaskperm.manage_webhooks = botaskperm.manage_emojis = botaskperm.manage_nicknames = botaskperm.move_members = False
        url = discord.utils.oauth_url(str(self.bot.user.id), botaskperm)
        self.logger.info("invite url : %s", url)
        print(url)

    @commands.check(check_botowner)
    @commands.command()
    async def shutdown(self,ctx):
        await ctx.message.channel.send("You are requesting a shutdown, please ensure that you want to performe it by typing `confirm`")
        chk = lambda m: m.author == ctx.message.author and m.channel == ctx.message.channel and m.content.lower() == 'confirm'
        try: answer = await self.bot.wait_for('message',check=chk,timeout=60)
        except asyncio.TimeoutError: answer = None
        if answer is None:
            await ctx.message.channel.send("your request has timeout")
        else:
            self.logger.warning("Shutdown requested by %s",str(ctx.message.author))
            await self.bot.logout()
            sys.exit(0)
