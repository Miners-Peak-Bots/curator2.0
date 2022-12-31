from ...utils.msg import titlefy, linkify, titlefy_simple, boldify
from pyrogram.handlers import MessageHandler
import emoji
from pyrogram.enums import ParseMode
from pyrogram import filters
from user.utils import create_get_user
from bot.utils.user import get_target_user
from bot.utils.msg import (
    sched_cleanup
)
from django.conf import settings
CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def prep_log(user):
    if not user.logs.count():
        return ''
    response = []
    logs = user.logs.all()
    for log in logs:
        response.append(
            boldify(log.message)
        )
    response = '\n'.join(response)
    return '<code>' + response + '</code>'


def prep_message(user):
    text = '@MinersPeak <b>Curator Bot</b>\n--------------------\n'
    text = text + titlefy('User id', user.tele_id)
    text = text + titlefy('First name', user.first_name)
    text = text + titlefy_simple('Username', user.username_tag)

    uname = user.username_tag
    text = text + f'<code>{uname.upper()}</code>, <code>{uname.lower()}</code>\n'
    # text = text + titlefy_simple('Username variants', user.username_tag)

    country = None
    if user.country:
        country = emoji.emojize(f':{user.country}:'.title())
    text = text + titlefy('Country', country)
    text = (
        text + linkify('keybase.io', 'keybase.io', True) +
        ': ' + linkify(user.keybase_link, user.keybase) + '\n'
    )
    text = text + titlefy('Phone', user.ph_number, nl=True)
    text = text + titlefy('Email', user.email, nl=True)
    if user.verified:
        text = text + '\n' + emoji.emojize(
            ':check_mark_button: <code>Verified!</code>'
        )
    # text = text + '\n' + titlefy('Reputation', len(user.rep.select()))
    text = text + '------------' + '\n'
    warns = user.warning.count()
    text = text + titlefy('Warns', f'{warns}/5')
    banned_status = 'Yes' if user.banned else 'No'
    text = text + titlefy('Banned', banned_status)

    text = text + '------------' + '\n'
    text = text + '<b>User log:\n</b>\n'
    """
    Add the logs
    """
    logs = prep_log(user)
    text = text + logs
    return text


def handle_acheck(client, msg):
    admin, created = create_get_user(msg.from_user)
    if not admin.is_admin:
        msg.delete()
        return False

    try:
        member = get_target_user(msg)
    except Exception:
        reply = msg.reply_text('User not found')
        sched_cleanup(reply)
        return False

    response = prep_message(member)
    reply = client.send_message(
        chat_id=admin.tele_id,
        text=response,
        disable_web_page_preview=True,
        parse_mode=ParseMode.HTML
    )
    sched_cleanup(reply)


__HANDLERS__ = [
    MessageHandler(handle_acheck,
                   filters.command('acheck', prefixes=CMD_PREFIX)),
]


__HELP__ADMIN__ = (
    "$acheck: Check a user's status(admin only)"
    '    $acheck 5431231\n'
    '    $acheck @username\n'
    '    Reply to a user\'s message with $acheck'
)
