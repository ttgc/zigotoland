#!usr/bin/env python3.7
#-*-coding:utf-8-*-

from discord.ext import commands
from src.discord.checks import *
from src.utils.config import *
from src.games.poker.lobby import *
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

    @commands.command()
    async def invite(self,ctx):
        botaskperm = discord.Permissions(519232)
        url = discord.utils.oauth_url(str(self.bot.user.id), botaskperm)
        embd = discord.Embed(title="Zigoto Bot",description="Invite the bot in your server !",colour=discord.Color(int('3CD070',16)),url=url)
        embd.set_footer(text="Bot created by Ttgc and Trakozz",icon_url=self.bot.user.avatar_url)
        embd.set_image(url=self.bot.user.avatar_url)
        embd.set_author(name="Zigoto Team",icon_url="https://www.2tout2rien.fr/wp-content/uploads/2012/12/Pingouin.jpg",url=url)
        embd.add_field(name="Currently on :",value=str(len(self.bot.guilds))+" servers",inline=True)
        await ctx.message.channel.send(embed=embd)
        self.logger.info("invite url : %s", url)
        print(url)

    @commands.check(check_botowner)
    @commands.command()
    async def shutdown(self,ctx):
        await ctx.message.channel.send("You are requesting a shutdown, please ensure that you want to perform it by typing `confirm`")
        chk = lambda m: m.author == ctx.message.author and m.channel == ctx.message.channel and m.content.lower() == 'confirm'
        try: answer = await self.bot.wait_for('message',check=chk,timeout=60)
        except asyncio.TimeoutError: answer = None
        if answer is None:
            await ctx.message.channel.send("your request has timeout")
        else:
            pokerlobbyls = []
            for k in PokerLobby.instances.values(): pokerlobbyls.append(k)
            for i in pokerlobbyls:
                await i.disband()
            self.logger.warning("Shutdown requested by %s",str(ctx.message.author))
            await self.bot.logout()
            await client.close()
            sys.exit(0)

    @commands.check(check_botowner)
    @commands.command()
    async def destroy(self,ctx):
        await ctx.message.channel.send("You are requesting to destroy the current financial district server, please ensure that you want to perform it by typing `confirm`")
        chk = lambda m: m.author == ctx.message.author and m.channel == ctx.message.channel and m.content.lower() == 'confirm'
        try: answer = await self.bot.wait_for('message',check=chk,timeout=60)
        except asyncio.TimeoutError: answer = None
        if answer is None:
            await ctx.message.channel.send("your request has timeout")
        else:
            self.logger.warning("Destroy requested by %s",str(ctx.message.author))
            config = Config()
            await config.guild.delete()
            await self.bot.logout()
            await client.close()
            sys.exit(0)

    @commands.command()
    async def opendeal(self,ctx):
        config = Config()
        invite = await config.guild.text_channels[0].create_invite(max_age=3600,reason="Create invite")
        self.logger.info("Created invite to self-guild : %s",invite.url)
        print(invite.url)
        await ctx.channel.send("Welcome to the financial district : \n{}".format(invite.url))
