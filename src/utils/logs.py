#!usr/bin/env python3.7
#-*-coding:utf-8-*-

import logging,os

class DebugFilter(logging.Filter):
    def filter(self,record):
        return record.levelno == logging.DEBUG+1

global logger

def initlogs():
    global logger
    if not os.access("Logs",os.F_OK):
        os.mkdir("Logs")
    logger = logging.getLogger('discord')
    # basic handler (all)
    logging.basicConfig(level=logging.DEBUG+1)
    handler = logging.FileHandler(filename='Logs/all.log', encoding='utf-8', mode='a')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    # latest logs
    handler = logging.FileHandler(filename='Logs/latest.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    # error logs
    handler = logging.FileHandler(filename='Logs/errors.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    handler.setLevel(logging.ERROR)
    logger.addHandler(handler)
    # debug logs
    handler = logging.FileHandler(filename='Logs/debug.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    handler.addFilter(DebugFilter())
    logger.addHandler(handler)
    return logger

def getlogger():
    global logger
    return logger
