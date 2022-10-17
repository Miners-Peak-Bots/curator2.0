from pyrogram.handlers import MessageHandler
from pyrogram import filters
from pyrogram.enums import ParseMode
from user.models import (
    TeleUser,
)


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

    print(is_admin)
    response = '\n\n'.join(help_)
    response = f'<code>{response}</code>'
    msg.reply(
        text=response,
        parse_mode=ParseMode.HTML
    )


__HANDLERS__ = [
    MessageHandler(handle_help,
                   (filters.command(['help', 'commands'], prefixes='!')
                    &
                    filters.private))
]


__HELP__ = (
    '!help/!commands - Send list of all avialable commands and usage'
)
