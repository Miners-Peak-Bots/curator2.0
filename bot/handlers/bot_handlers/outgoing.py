from pyrogram.handlers import MessageHandler
from pyrogram import filters


def handle_outgoing(client, msg):
    print('outgoing msg, gott delete it later')
    print(msg)


__HANDLERS__ = [
    [MessageHandler(handle_outgoing, filters.outgoing), -1]
]

__HELP__ = ''
