from bot.utils.msg import titlefy, linkify, titlefy_simple, boldify
import emoji
from .models import TeleUser
from datetime import datetime, timedelta
from pyrogram.types import ChatPermissions


def create_user(member):
    return TeleUser.objects.create(
        tele_id=member.id,
        username=member.username,
        first_name=member.first_name,
        last_name=member.last_name
    )


def create_get_user(member):
    return TeleUser.objects.get_or_create(
        tele_id=member.id,
        defaults={
            'username': member.username,
            'first_name': member.first_name,
            'last_name': member.last_name
        }
    )


def ban_user(client, user_id, chat_id):
    """
    This is a permanent ban since no `until_date` is specified
    """
    try:
        client.ban_chat_member(
            chat_id=chat_id,
            user_id=user_id
        )
    except Exception:
        raise


def unban_user(client, user_id, chat_id):
    try:
        client.unban_chat_member(
            chat_id=chat_id,
            user_id=user_id
        )
    except Exception:
        raise


def mute_user(client, chat_id, user_id, duration=30):
    until = datetime.now() + timedelta(days=duration)
    client.restrict_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        permissions=ChatPermissions(),
        until_date=until
    )


def prep_check(user):
    text = '@MinersPeak <b>Curator Bot</b>\n--------------------\n'
    if user.verified:
        text = text + emoji.emojize(
            ':check_mark_button: VERIFIED :check_mark_button:\n\n'

        )
    else:
        text = text + emoji.emojize(
            ':prohibited: NOT VERFIEID :prohibited:\n\n'
        )
    text = text + titlefy('User id', user.tele_id)
    if user.first_name:
        text = text + f'First name: {user.first_name}\n'
    if user.username:
        uname = user.username_tag
        text = text + f'Username: {uname}\n'
        text = text + f'<code>{uname.upper()}</code>, <code>{uname.lower()}</code>\n'
        text = text + '\n'

    if user.country:
        country = emoji.emojize(f':{user.country}:'.title())
        text = text + f'Country: {country}\n'
    else:
        text = text + f'Country: {user.country}\n'

    text = (
        text + linkify('keybase.io', 'keybase.io', True) +
        ': ' + linkify(user.keybase_link, user.keybase) + '\n'
    )
    return text


def prep_user_log(user):
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


def prep_acheck(user):
    text = '@MinersPeak <b>Curator Bot</b>\n--------------------\n'
    if user.verified:
        text = text + emoji.emojize(
            ':check_mark_button: VERIFIED :check_mark_button:\n\n'

        )
    else:
        text = text + emoji.emojize(
            ':prohibited: NOT VERFIEID :prohibited:\n\n'
        )
    text = text + titlefy('User id', user.tele_id)
    text = text + titlefy('First name', user.first_name)
    text = text + titlefy_simple('Username', user.username_tag)

    uname = user.username_tag
    text = text + f'<code>{uname.upper()}</code>, <code>{uname.lower()}</code>\n'
    text = text + '\n'
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
    logs = prep_user_log(user)
    text = text + logs
    return text
