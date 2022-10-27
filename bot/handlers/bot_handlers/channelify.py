from pyrogram.handlers import MessageHandler
from pyrogram.types import ChatPermissions
from pyrogram import filters
from django.conf import settings
from django.conf.settings import (
    BOT_COMMAND_PREFIX as CMD_PREFIX
)


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
                   filters.command('channelmode', prefixes=CMD_PREFIX)),
    MessageHandler(handle_group_mode,
                   filters.command('groupmode', prefixes=CMD_PREFIX)),
]


__HELP__ADMIN__ = (
    '$channelmode: Switch a group to channel mode where only admins can post\n'
    '    Send $channelmode in a group\n'
    '$groupmode: Switch a group back to group mode where everybody can post'
    '    Send $groupmode in a group\n'
)
