from .core import bot
from pyrogram import idle
from .sched import jobs


def initialize():
    jobs.start()
    bot.start()
    idle()
