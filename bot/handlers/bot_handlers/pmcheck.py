from ...utils.msg import titlefy, linkify, titlefy_simple, boldify
from pyrogram.handlers import MessageHandler
from user.utils import create_get_user
from pyrogram import filters
from pyrogram.enums import ParseMode
import emoji
from user.models import (
    TeleUser
)


def prep_message_user(user):
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


def prep_message_admin(user):
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


def pm_check(client, msg):
    if msg.forward_sender_name:
        return msg.reply_text(f'{msg.forward_sender_name} has forward privacy enabled')
    elif msg.forward_from:
        target = msg.forward_from

        try:
            user = TeleUser.objects.get(pk=target.id)
        except TeleUser.DoesNotExist:
            user = TeleUser.objects.create(
                tele_id=target.id,
                first_name=target.first_name,
                last_name=target.last_name,
                username=target.username
            )

        """
        update details of the user
        """
        user.first_name = target.first_name
        user.last_name = target.last_name
        user.username = target.username
        user.save()
        try:
            current_user = TeleUser.objects.get(pk=msg.from_user.id)
        except TeleUser.DoesNotExist:
            return msg.reply('You do not have the rights to run this operation')

        if current_user.is_admin:
            response = prep_message_admin(user)
        else:
            response = prep_message_user(user)

        return client.send_message(
            chat_id=msg.from_user.id,
            text=response,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    else:
        msg.reply('Unknown error occured, could not find user')


__HANDLERS__ = [
    MessageHandler(pm_check, (filters.forwarded & filters.private)),
]
