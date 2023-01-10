from pyrogram.handlers import MessageHandler
from pyrogram import filters


def handle_start(client, msg):
    if len(msg.command) > 1:
        """
        This is a deep linked message for reviewing sellers.
        Pass to another method
        """
        # await handle_review(client, msg)
        return False

    msg.reply_text('I am a private group administration robot.')


__HANDLERS__ = [
    MessageHandler(handle_start, filters.command('start', '/'))
]
