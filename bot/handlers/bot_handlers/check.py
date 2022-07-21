from pyrogram.handlers import MessageHandler
import emoji
from pyrogram import filters
from bot.utils.user import get_target_user


def prep_message(user):
    text = f'User id: {user.tele_id}\n'
    if user.first_name:
        text = text + f'First name: {user.first_name}\n'
    if user.username:
        text = text + f'Username: @{user.username}\n'
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
        return msg.reply_text('User not found')

    response = prep_message(member)
    msg.reply_text(response)


__HANDLERS__ = [
    MessageHandler(handle_check, filters.command('check', prefixes='!'))
]


__HELP__ = (
    '!check: Retrieve public information about a user\n'
    '   !check 521231\n'
    '   !check @username\n'
    "   Reply to a user's message with !check\n"
)
