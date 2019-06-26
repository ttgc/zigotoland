#!usr/bin/env python3.7
#-*-coding:utf-8-*-

import discord
from discord.ext import commands

class Help(commands.HelpCommand):
    def __init__(self):
        commands.HelpCommand.__init__(self)
        self.verify_checks = True

    async def prepare_help_command(self,ctx,command=None):
        self.cog = self.context.bot.get_cog("Utils")
        commands.HelpCommand.prepare_help_command(self,ctx,command)

    async def commands_not_found(self,string):
        return "Command {} not found".format(string)

    async def subcommand_not_found(self,command,string):
        if isinstance(command,commands.Group):
            return "Subcommand {} of command {} does not exist".format(string,command.qualified_name)
        return "The command {} has no subcommands".format(command.qualified_name)

    async def filter_commands(self,cmdlist,*,sort=False,key=None):
        cmdlist = await commands.HelpCommand.filter_commands(self,cmdlist,sort=sort,key=key)
        finalcmdlist = []
        for cmd in cmdlist:
            curlist = []
            if isinstance(cmd,commands.Group):
                if cmd.invoke_without_command: finalcmdlist.append(cmd)
                for cmdgrp in cmd.commands:
                    finalcmdlist.append(cmdgrp)
            else:
                finalcmdlist.append(cmd)
            finalcmdlist += curlist
        return finalcmdlist

    async def send_bot_help(self,mapping):
        embd = discord.Embed(title="Zigoto Bot",description="List of commands avalaible",colour=discord.Color(int('3CD070',16)),url="https://github.com/ttgc/zigotoland")
        embd.set_footer(text="Made by Zigoto Team")
        embd.set_author(name="Zigoto Bot",icon_url=self.context.bot.user.avatar_url)
        for i,k in mapping.items():
            k = await self.filter_commands(k,sort=True)
            ls = []
            for cmd in k:
                ls.append(cmd.qualified_name)
            if len(ls) == 0: ls = ["None"]
            if i is not None: embd.add_field(name=i.qualified_name,value="\n".join(ls),inline=True)
        await self.get_destination().send(embed=embd)

    async def send_cog_help(self,cog):
        embd = discord.Embed(title="Zigoto Bot",description="List of commands avalaible in group {}".format(cog.qualified_name),colour=discord.Color(int('3CD070',16)),url="https://github.com/ttgc/zigotoland")
        embd.set_footer(text="Made by Zigoto Team")
        embd.set_author(name="Zigoto Bot",icon_url=self.context.bot.user.avatar_url)
        ls = await self.filter_commands(cog.get_commands(),sort=True)
        for i in ls:
            embd.add_field(name=i.qualified_name,value=self.get_command_signature(i),inline=True)
        await self.get_destination().send(embed=embd)

    async def send_command_help(self,command):
        embd = discord.Embed(title="Zigoto Bot",description="Help on command {}".format(command.qualified_name),colour=discord.Color(int('3CD070',16)),url="https://github.com/ttgc/zigotoland")
        embd.set_footer(text="Made by Zigoto Team")
        embd.set_author(name="Zigoto Bot",icon_url=self.context.bot.user.avatar_url)
        embd.add_field(name="Prototype :",value=self.get_command_signature(command),inline=False)
        embd.add_field(name=self."Description :",value=command.help,inline=False)
        await self.get_destination().send(embed=embd)

    async def send_group_help(self,group):
        embd = discord.Embed(title="Zigoto Bot",description="List of commands avalaible in group {}".format(group.qualified_name),colour=discord.Color(int('3CD070',16)),url="https://github.com/ttgc/zigotoland")
        embd.set_footer(text="Made by Zigoto Team")
        embd.set_author(name="Zigoto Bot",icon_url=self.context.bot.user.avatar_url)
        for cmd in group.commands:
            embd.add_field(name=cmd.qualified_name,value=self.get_command_signature(cmd),inline=True)
        await self.get_destination().send(embed=embd)
