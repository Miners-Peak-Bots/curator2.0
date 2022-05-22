from ...db.cache import users_cache, groups_cache
from ...db.models import Group, User, UserLog
from ...utils.msg import errorify
from pyrogram.handlers import MessageHandler
import os
import emoji
import peewee
from pyrogram import filters


__HELP__ = """Hey man
How is it going"""


def handle_unverify(client, msg):
    if msg.from_user.id != client.config.general.master_id:
        msg.delete()
        return False

    if not msg.reply_to_message:
        msg.delete()
        return False

    if not msg.reply_to_message.forward_from:
        msg.delete()
        return False

    reason = msg.text.replace('!unverify', '').strip()
    if not len(reason) > 0:
        msg.reply_text('Please provide a valid reason')
        return False

    reply_to = msg.reply_to_message
    user_id = reply_to.forward_from.id

    try:
        user = User.get(User.user_id == user_id)
    except peewee.DoesNotExist:
        msg.reply_text('User not found in database')
        return False

    if not user.verified:
        msg.reply_text('User is not verified.')
        return False

    user.verified = False
    user.save()
    log = UserLog(user=user,
                  message=reason)
    log.save()

    errors = []
    for group in Group.select():
        try:
            client.promote_chat_member(chat_id=group.group_id,
                                       user_id=user.user_id,
                                       can_manage_chat=False)
        except Exception as e:
            errors.append(
                f'Could not remove as admin in {group.group_id} due to\n'
                f'{str(e)}'
            )

    response = errorify('User has been removed from verified users', errors)
    msg.reply_text(response)


async def handle_verify(client, msg):
    if msg.from_user.id != client.config.general.master_id:
        msg.delete()
        return False

    if not msg.reply_to_message:
        msg.delete()
        return False

    if not msg.reply_to_message.forward_from:
        msg.delete()
        return False

    reply_to = msg.reply_to_message
    user_id = reply_to.forward_from.id

    try:
        user = User.get(User.user_id == user_id)
    except peewee.DoesNotExist:
        msg.reply_text('User not found in database')
        return False

    try:
        flagg = msg.command[1]
    except IndexError:
        msg.reply_text('Please mention a country')
        return False

    try:
        phone = msg.command[2]
    except IndexError:
        msg.reply_text('Please mention a phone number')
        return False

    try:
        email = msg.command[3]
    except IndexError:
        msg.reply_text('Please mention an email')
        return False

    try:
        keybase = msg.command[4]
    except IndexError:
        msg.reply_text('Please mention a valid keybase address')
        return False

    country = emoji.demojize(flagg).replace(':', '').strip().lower()

    user.country = country
    user.keybase = os.path.basename(keybase)
    user.email = email
    user.ph_number = phone
    user.verified = True
    user.save()

    """
    Promote user to admin and set admin title
    """
    errors = []
    for group in Group.select():
        try:
            client.promote_chat_member(chat_id=group.group_id,
                                       user_id=user.user_id,
                                       can_pin_messages=True)

            client.set_administrator_title(group.group_id, user.user_id,
                                           'Curator verified')
        except Exception as e:
            errors.append(
                f'Could not promote in {group.group_id} due to\n'
                f'{str(e)}. Please fix manually or retry.'
            )

    response = errorify('User has been verified', errors)
    await msg.reply_text(response)


__HANDLERS__ = [
    MessageHandler(handle_verify,
                   (filters.command('verify', prefixes='!') &
                    filters.private)),
    MessageHandler(handle_unverify,
                   (filters.command('unverify', prefixes='!') &
                    filters.private)),
]
