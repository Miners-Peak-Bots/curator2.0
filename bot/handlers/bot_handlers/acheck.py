from ...db.cache import users_cache, groups_cache
from ...db.models import User
from ...utils.user import get_user, create_user
from ...utils.msg import titlefy, linkify, titlefy_simple, boldify
from pyrogram.handlers import MessageHandler
import emoji
import peewee
from pyrogram import filters


__HELP__ = """Hey man
How is it going"""


def prep_log(user):
    response = []
    logs = user.log.select()
    for log in logs:
        response.append(
            boldify(log.message + ' on ' + log.date.strftime('%m/%d/%Y'))
        )
    response = '\n'.join(response)
    return '<code>' + response + '</code>'


def prep_message(user):
    text = '@MinersPeak <b>Curator Bot</b>\n--------------------\n'
    text = text + titlefy('User id', user.user_id)
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
    text = text + '\n' + titlefy('Reputation', len(user.rep.select()))
    text = text + '------------' + '\n'
    warns = len(user.warns.select())
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


async def handle_acheck(client, msg):
    if not msg.reply_to_message:
        return False

    """
    if the command is not from master
    fetch the current user and check if they are an admin
    """
    master = client.config.general.master_id
    if msg.from_user.id != master:
        try:
            user = get_user(msg.from_user.id)
            if not user.admin:
                await msg.delete()
                return False
        except peewee.DoesNotExist:
            await msg.delete()
            return False

    target_user = msg.reply_to_message.from_user
    member_id = target_user.id
    try:
        member = get_user(member_id)
    except peewee.DoesNotExist:
        member = create_user(target_user)

    response = prep_message(member)
    await msg.reply_text(response, parse_mode="html")


__HANDLERS__ = [
    MessageHandler(handle_acheck, filters.command('acheck', prefixes='!')),
]
