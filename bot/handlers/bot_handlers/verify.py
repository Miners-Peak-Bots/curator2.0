from ...utils.msg import errorify
from user.utils import create_get_user
from group.models import Group
from django.conf import settings
from pyrogram.handlers import MessageHandler
import os
import emoji
from pyrogram import filters

from user.models import (
    TeleUser,
)

CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def is_allowed(msg):
    try:
        TeleUser.objects.get(pk=msg.from_user.id, helper_admin=True)
    except TeleUser.DoesNotExist:
        if msg.from_user.id not in settings.BOT_MASTER:
            msg.delete()
            return False

    if not msg.reply_to_message:
        msg.reply_text('reply to a message')
        msg.delete()
        return False

    if not msg.reply_to_message.forward_from:

        if msg.reply_to_message.forward_sender_name is not None:
            msg.reply_text(
                f"user {msg.reply_to_message.forward_sender_name} need to change privacy settings for forward message to everyone"
            )
        else:
            msg.reply_text("reply to a forwarded message")

        msg.delete()
        return False

    return True


def handle_unverify(client, msg):

    if not is_allowed(msg):
        return False

    reason = msg.text.replace('$unverify', '').strip()
    if not len(reason) > 0:
        msg.reply_text('Please specify a reason')
        return False

    reply_to = msg.reply_to_message
    user, created = create_get_user(reply_to.forward_from)

    if not user.verified:
        msg.reply_text('User is not verified.')
        return False

    user.verified = False
    user.save()

    errors = []
    for group in Group.objects.filter(vendor=True).all():
        privileges = group.get_special_privileges()
        try:
            client.promote_chat_member(chat_id=group.group_id, user_id=user.tele_id, privileges=privileges)
        except Exception as e:
            errors.append(f'Could not unverify in {group.title}({group.group_id}) due to\n' f'{str(e)}')

    response = errorify('User has been removed from verified users', errors)
    msg.reply_text(response)


def handle_verify(client, msg):

    if not is_allowed(msg):
        return False

    reply_to = msg.reply_to_message
    user, created = create_get_user(reply_to.forward_from)
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
    for group in Group.objects.filter(vendor=True).all():
        try:
            privileges = group.get_special_privileges()
            client.promote_chat_member(chat_id=group.group_id, user_id=user.tele_id, privileges=privileges)
        except Exception as e:
            errors.append(
                f'Could not verify in {group.title}({group.group_id}) due to\n'
                f'{str(e)}. Please fix manually or retry.'
            )

        try:
            if group.flair:
                print("Setting flair to ", group.flair)
                client.set_administrator_title(group.group_id, user.tele_id, group.flair)
        except Exception as e:
            errors.append(
                f'Could not set flair in {group.title}({group.group_id}) due to\n'
                f'{str(e)}. Please fix manually or retry.'
            )

    response = errorify('User has been verified', errors)
    msg.reply_text(response)


__HANDLERS__ = [
    MessageHandler(handle_verify, filters.command('verify', prefixes=CMD_PREFIX)),
    MessageHandler(handle_unverify, filters.command('unverify', prefixes=CMD_PREFIX)),
]

__HELP__ADMIN__ = (
    '$verify: Promote a user to verified seller status\n'
    '    Respond to a forwarded message of a user in private to verify\n'
    '    $verify 🇺🇸 +14332334234 user@mail.com keybase.io/username\n'
    '$unverify: Remove a user from verified seller status\n'
    '    Respond to a forwarded message of a user in private to unverify\n'
)
