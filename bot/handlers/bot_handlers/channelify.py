from pyrogram.handlers import MessageHandler
from pyrogram.types import ChatPermissions
from pyrogram import filters
from django.conf import settings


__HELP__ = """Hey man
How is it going"""


def handle_channel_mode(client, msg):
    if msg.from_user.id != settings.BOT_MASTER:
        msg.delete()
        return False

    client.set_chat_permissions(msg.chat.id, ChatPermissions())
    msg.reply_text('Channel mode enabled')


def handle_group_mode(client, msg):
    if msg.from_user.id != settings.BOT_MASTER:
        msg.delete()
        return False

    client.set_chat_permissions(msg.chat.id,
                                ChatPermissions(
                                    can_send_messages=True,
                                    can_send_media_messages=True
                                ))
    msg.reply_text('Channel mode disabled')


__HANDLERS__ = [
    MessageHandler(handle_channel_mode,
                   filters.command('channelmode', prefixes='!')),
    MessageHandler(handle_group_mode,
                   filters.command('groupmode', prefixes='!')),
]
