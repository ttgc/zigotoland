#!usr/bin/env python3.7
#-*-coding:utf-8-*-

import discord

class DatabaseException(Exception):
    pass

class NoChannelFoundException(DatabaseException):
    def __init__(self,channel: discord.TextChannel):
        super()
        self.channel = channel

class NoEntryFoundException(DatabaseException):
    def __init__(self,searching):
        super()
        self.entry = searching

class TableDoesNotExist(DatabaseException):
    def __init__(self,db,table):
        super()
        self.database = db
        self.table = table

class TableAlreadyExist(DatabaseException):
    def __init__(self,db,table):
        super()
        self.database = db
        self.table = table

class DatabaseDoesNotExist(DatabaseException):
    def __init__(self,db):
        super()
        self.database = db

class DatabaseAlreadyExist(DatabaseException):
    def __init__(self,db):
        super()
        self.database = db

class ServerNotFoundException(DatabaseException):
    def __init__(self,srvid):
        super()
        self.serverID = srvid
