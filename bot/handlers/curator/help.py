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


def handle_help(client, msg):
    response = '\n\n'.join(client.help)
    response = f'<code>{response}</code>'

    is_admin = False
    try:
        admin = TeleUser.objects.get(pk=msg.from_user.id)
        is_admin = admin.is_admin
    except TeleUser.DoesNotExist:
        pass

    if is_admin:
        help_ = client.help + client.admin_manual
    else:
        help_ = client.help

    help_text = '\n\n'.join(help_)

    if not is_admin:
        response = f'<code>{response}</code>'
        msg.reply(
            text=response,
            parse_mode=ParseMode.HTML
        )
    else:
        if not os.path.isfile('help-full.txt'):
            with open('help-full.txt', 'w') as f:
                f.write(help_text)
        client.send_document(
            chat_id=msg.chat.id,
            document='help-full.txt'
        )



__HANDLERS__ = [
    MessageHandler(handle_help,
                   (filters.command(['help', 'commands'], prefixes=CMD_PREFIX)
                    &
                    filters.private))
]


__HELP__ = (
    '$help/$commands - Send list of all avialable commands and usage'
)
