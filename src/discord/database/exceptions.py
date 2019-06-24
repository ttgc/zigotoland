#!usr/bin/env python3.7
#-*-coding:utf-8-*-

import discord

class DatabaseException(Exception):
    pass

class NoChannelFoundException(DatabaseException):
    def __init__(self,channel: discord.TextChannel):
        self.super()
        self.channel = channel

class NoEntryFoundException(DatabaseException):
    def __init__(self,searching):
        self.super()
        self.entry = searching

class TableDoesNotExist(DatabaseException):
    def __init__(self,db,table):
        self.super()
        self.database = db
        self.table = table

class TableAlreadyExist(DatabaseException):
    def __init__(self,db,table):
        self.super()
        self.database = db
        self.table = table

class DatabaseDoesNotExist(DatabaseException):
    def __init__(self,db):
        self.super()
        self.database = db

class DatabaseAlreadyExist(DatabaseException):
    def __init__(self,db):
        self.super()
        self.database = db

class ServerNotFoundException(DatabaseException):
    def __init__(self,srvid):
        self.super()
        self.serverID = srvid
