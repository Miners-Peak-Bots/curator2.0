from pyrogram.handlers import MessageHandler
from pyrogram import filters
from pyrogram.enums import ParseMode
from user.models import (
    TeleUser,
)
from django.conf import settings
import os
import textwrap

CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def is_admin(user_id):
    if user_id in settings.BOT_MASTER:
        return True

    try:
        admin = TeleUser.objects.get(pk=user_id)
        return admin.is_admin
    except TeleUser.DoesNotExist:
        return False


def handle_help(client, msg):
    if is_admin(msg.from_user.id):
        help_ = client.help + client.admin_manual
        help_text = "\n\n".join(help_)
        with open("help-full.txt", "w") as f:
            f.write(help_text)
        client.send_document(chat_id=msg.chat.id, document="help-full.txt")

    else:
        response = "\n\n".join(client.help)
        response = f"<code>{response}</code>"
        msg.reply(text=response, parse_mode=ParseMode.HTML)


__HANDLERS__ = [
    MessageHandler(
        handle_help,
        (filters.command(["help", "commands"], prefixes=CMD_PREFIX) & filters.private),
    )
]


__HELP__ = "$help/$commands - Send list of all avialable commands and usage(in DM)"
