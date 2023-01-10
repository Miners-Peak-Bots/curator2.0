from pyrogram.handlers import MessageHandler
from pyrogram import filters


def cleanup_servicemsg(client, msg):
    msg.delete()


__HANDLERS__ = [
    MessageHandler(cleanup_servicemsg, filters.service),
]
