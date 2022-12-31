from pyrogram.handlers import MessageHandler
import emoji
from pyrogram import filters
from bot.utils.user import get_target_user
from bot.utils.msg import (
    sched_cleanup
)
from django.conf import settings
CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def prep_message(user):
    text = f'User id: {user.tele_id}\n'
    if user.first_name:
        text = text + f'First name: {user.first_name}\n'
    if user.username:
        uname = user.username_tag
        text = text + f'Username: {uname}\n'
        text = text + f'<code>{uname.upper()}</code>, <code>{uname.lower()}</code>\n'
    if user.country:
        country = emoji.emojize(f':{user.country}:'.title())
        text = text + f'Country: {country}\n'
    if user.verified:
        text = text + emoji.emojize(':check_mark_button: Verified')

    return text


def handle_check(client, msg):
    try:
        member = get_target_user(msg)
    except Exception:
        reply = msg.reply_text('User not found')
        sched_cleanup(reply)
        return False

    response = prep_message(member)
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
