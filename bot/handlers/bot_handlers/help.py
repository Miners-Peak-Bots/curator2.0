from pyrogram.handlers import MessageHandler
from pyrogram import filters
from pyrogram.enums import ParseMode


def handle_help(client, msg):
    msg.reply('\n'.join(client.help))
    response = '\n\n'.join(client.help)
    response = f'<code>{response}</code>'
    msg.reply(
        text=response,
        parse_mode=ParseMode.HTML
    )


__HANDLERS__ = [
    MessageHandler(handle_help,
                   filters.command(['help', 'commands'], prefixes='!'))
]


__HELP__ = (
    '!help/!commands - Send list of all avialable commands and usage'
)
