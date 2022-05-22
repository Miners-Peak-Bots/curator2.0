from .core import bot
from pyrogram import idle


def initialize():
    bot.start()
    idle()
