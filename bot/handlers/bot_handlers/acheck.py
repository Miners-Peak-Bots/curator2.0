from ...utils.msg import titlefy, linkify, titlefy_simple, boldify
from pyrogram.handlers import MessageHandler
import emoji
from pyrogram.enums import ParseMode
from pyrogram import filters
from bot.utils.user import get_target_user


def prep_log(user):
    response = []
    logs = user.logs.all()
    for log in logs:
        response.append(
            boldify(log.message + ' on ' + log.date.strftime('%m/%d/%Y'))
        )
    response = '\n'.join(response)
    return '<code>' + response + '</code>'


def prep_message(user):
    text = '@MinersPeak <b>Curator Bot</b>\n--------------------\n'
    text = text + titlefy('User id', user.tele_id)
    text = text + titlefy('First name', user.first_name)
    text = text + titlefy_simple('Username', user.username_tag)

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
    text = text + titlefy('Warns', f'{warns}/3')
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
    if not msg.reply_to_message:
        return False

    admin, created = create_get_user(msg.from_user)
    if not admin.is_admin:
        msg.delete()
        return False

    try:
        member = get_target_user(msg)
    except Exception:
        return msg.reply_text('User not found')
    response = prep_message(member)
    msg.reply_text(response, parse_mode=ParseMode.HTML)


__HANDLERS__ = [
    MessageHandler(handle_acheck, filters.command('acheck', prefixes='!')),
]


__HELP__ = (
    "!acheck: Check a user's status(admin only)"
    '    !acheck 5431231\n'
    '    !acheck @username\n'
    '    Reply to a user\'s message with !acheck'
)
