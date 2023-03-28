from pyrogram.handlers import MessageHandler
from pyrogram.enums import ParseMode
from pyrogram import filters
from user.models import TeleUser
from django.conf import settings
CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def handle_verified(client, msg):
    verified_l = TeleUser.objects.filter(verified=True)
    message = []
    for user in verified_l:
        message.append(user.mention)
    response = '\n'.join(message)
    msg.reply_text(response)
    pass


__HANDLERS__ = [
    MessageHandler(handle_verified,
                   (
                       filters.command('verified', prefixes=CMD_PREFIX)
                       &
                       filters.private
                   )),
]


__HELP__ = (
    "$verified: Print a list of verified users"
)
