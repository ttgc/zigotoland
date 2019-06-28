#!usr/bin/env python3.7
#-*-coding:utf-8-*-

import discord
from discord.ext import commands
import logging

async def manage_roles(ctx, logger):
    gold = discord.utils.get(ctx.guild.roles, name="Gold")
    plat = discord.utils.get(ctx.guild.roles, name="Platinium")
    dark = discord.utils.get(ctx.guild.roles, name="Darkness")
    reorganize = False
    if gold is None:
        gold = await ctx.guild.create_role(name="Gold",
                        permissions=ctx.guild.default_role.permissions,
                        color=discord.Color(int("FFD700",16)), hoist=True,
                        mentionable=True, reason="Creating Gold role")
        logger.info("Create Gold role : %d",gold.id)
        reorganize = True
    if plat is None:
        perms = ctx.guild.default_role.permissions
        perms.manage_channels = perms.priority_speaker = perms.send_tts_messages = perms.manage_messages = True
        plat = await ctx.guild.create_role(name="Platinium",
                        permissions=perms, color=discord.Color(int("C2C2C2",16)),
                        hoist=True, mentionable=True, reason="Creating Platinium role")
        logger.info("Create Platinium role : %d",plat.id)
        reorganize = True
    if plat is None:
        plat = await ctx.guild.create_role(name="Platinium",
                        permissions=plat.permissions, color=discord.Color(int("010101",16)),
                        hoist=True, mentionable=True, reason="Creating Darkness role")
        logger.info("Create Darkness role : %d",plat.id)
        reorganize = True
    if reorganize:
        position = {"Gold":0, "Platinium":1, "Darkness": 2}
        for i in ctx.guild.roles:
            if i.name in position:
                await i.edit(position=position[i.name])
    return gold, plat, dark
