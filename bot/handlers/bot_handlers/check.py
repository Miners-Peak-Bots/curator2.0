from pyrogram.handlers import MessageHandler
from pyrogram import filters
from bot.utils.user import get_target_user
from bot.utils.msg import (
    sched_cleanup
)
from user.utils import (
    prep_check
)
from django.conf import settings
CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def handle_check(client, msg):
    try:
        member = get_target_user(msg)
    except Exception:
        reply = msg.reply_text('User not found')
        sched_cleanup(reply)
        return False

    # response = prep_message(member)
    response = prep_check(member)
    reply = msg.reply_text(response)
    sched_cleanup(reply)


__HANDLERS__ = [
    MessageHandler(handle_check, filters.command('check', prefixes=CMD_PREFIX))
]


__HELP__ = (
    '$check: Retrieve public information about a user\n'
    '   $check 521231\n'
    '   $check @username\n'
    "   Reply to a user's message with $check\n"
)
