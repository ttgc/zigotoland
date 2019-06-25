#!usr/bin/env python3.7
#-*-coding:utf-8-*-

import discord

class DataFormat:
    def __init__(self,*data):
        self.data = data

    def __getitem__(self,item):
        return self.data[item]

    def __setitem__(self,item,value):
        self.data[item] = value

    def __str__(self):
        return "|@|".join(self.data)

    async def send(self,channel):
        await channel.send(str(self))

    @classmethod
    def parse(cl,string):
        return cl(*string.split("|@|"))
