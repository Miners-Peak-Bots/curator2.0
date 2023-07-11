from ...utils.msg import errorify
from user.utils import create_get_user
from group.models import Group
from django.conf import settings
from pyrogram.handlers import MessageHandler
import os
import emoji
from pyrogram import filters

from .acheck import handle_acheck
from user.models import (
    TeleUser,
)

from pyrogram.types import ChatPrivileges
from pyrogram.errors import ChatAdminRequired, UserPrivacyRestricted


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

    if msg.reply_to_message.forward_sender_name is not None:
        msg.reply_text(f"user {msg.reply_to_message.forward_sender_name} need to change privacy settings for forward message to everyone")
        msg.delete()
        return False

    elif not msg.reply_to_message.forward_from:
        msg.reply_text("reply to a forwarded message")
        msg.delete()
        return False

    return True


"""
This function helps get the target user
of the verify command and also checks if the message is allowed and throws an
exception if not
"""


def is_allowed_and_get_target(msg):
    try:
        TeleUser.objects.get(pk=msg.from_user.id, helper_admin=True)
    except TeleUser.DoesNotExist:
        if msg.from_user.id not in settings.BOT_MASTER:
            raise Exception('You need to be an admin to use this command')

    if not msg.reply_to_message:
        raise Exception('You need to use this command as a response')

    # Target message
    tmsg = msg.reply_to_message

    if tmsg.forward_sender_name is not None:
        raise Exception(f'{tmsg.forward_sender_name} has to disable their forward privacy')
    elif tmsg.forward_from:
        target = tmsg.forward_from
    elif not tmsg.forward_from and not tmsg.forward_sender_name:
        target = tmsg.from_user

    return target


def handle_unverify(client, msg):
    # if not is_allowed(msg):
    #     return False

    try:
        target = is_allowed_and_get_target(msg)
    except Exception as e:
        msg.reply_text(e)
        msg.delete()
        return False

    reason = msg.text.replace('$unverify', '').strip()
    if not len(reason) > 0:
        msg.reply_text('Please specify a reason')
        return False

    user, created = create_get_user(target)

    if not user.verified:
        msg.reply_text('User is not verified.')
        return False

    user.verified = False
    user.save()
    user.verify_log(message=reason, event=2)

    errors = []

    privileges = ChatPrivileges(can_manage_chat=False)

    for group in Group.objects.filter(vendor=True).all():
        try:
            client.promote_chat_member(chat_id=group.group_id, user_id=user.tele_id, privileges=privileges)

        except ChatAdminRequired:
            errors.append(
                f'Could not unverify in {group.title}({group.group_id}) as bots cant edit admins promoted by other admins\n Demote them and try again'
            )

        except UserPrivacyRestricted:
            errors.append(f'Can not demote in {group.title}({group.group_id}) as {msg.reply_to_message.forward_sender_name} isnt member of this group')

        except Exception as e:
            errors.append(f'Could not unverify in {group.title}({group.group_id}) due to\n' f'{str(e)}')

    response = errorify('User has been removed from verified users', errors)
    msg.reply_text(response)


def handle_verify(client, msg):
    # if not is_allowed(msg):
    #     return False
    target = is_allowed_and_get_target(msg)

    try:
        target = is_allowed_and_get_target(msg)
    except Exception as e:
        msg.reply_text(e)
        msg.delete()
        return False

    user, created = create_get_user(target)
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

    user.verify_log(event=1, message=None)

    """
    Promote user to admin and set admin title
    """

    errors = []

    for group in Group.objects.filter(vendor=True).all():
        privileges = group.get_special_privileges()

        try:
            client.promote_chat_member(chat_id=group.group_id, user_id=user.tele_id, privileges=privileges)

        except ChatAdminRequired:
            errors.append(
                f'Could not verify in {group.title}({group.group_id}) as bots cant edit admins promoted by other admins\n Demote them and try again'
            )

        except UserPrivacyRestricted:
            errors.append(f'Can not promote in {group.title}({group.group_id}) as {msg.reply_to_message.forward_sender_name} isnt member of this group')

        except Exception as e:
            errors.append(f'Could not verify in {group.title}({group.group_id}) due to\n' f'{str(e)}. Please fix manually or retry.')

        else:
            try:
                if group.flair:
                    print("Setting flair to ", group.flair)
                    client.set_administrator_title(group.group_id, user.tele_id, group.flair)
            except Exception as e:
                errors.append(f'Could not set flair in {group.title}({group.group_id}) due to\n' f'{str(e)}. Please fix manually or retry.')

    response = errorify('User has been verified', errors)
    msg.reply_text(response)
    handle_acheck(client, msg.reply_to_message, user_id=user.tele_id)


def handle_renew(client, msg):
    # if not is_allowed(msg):
    #     return False
    target = is_allowed_and_get_target(msg)

    try:
        target = is_allowed_and_get_target(msg)
    except Exception as e:
        msg.reply_text(e)
        msg.delete()
        return False

    user, created = create_get_user(target)

    if not user.verified:
        msg.reply_text('User is not verified and cannot be renewed')
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

    user.verify_log(event=3, message=None)
    msg.reply_text("User's verification has been renewed")
    handle_acheck(client, msg.reply_to_message, user_id=user.tele_id)


__HANDLERS__ = [
    MessageHandler(handle_verify, filters.command('verify', prefixes=CMD_PREFIX)),
    MessageHandler(handle_renew, filters.command('renew', prefixes=CMD_PREFIX)),
    MessageHandler(handle_unverify, filters.command('unverify', prefixes=CMD_PREFIX)),
]

__HELP__ADMIN__ = (
    '$verify: Promote a user to verified seller status\n'
    '    Respond to a forwarded message of a user in private to verify\n'
    '    $verify 🇺🇸 +14332334234 user@mail.com keybase.io/username\n'
    '$renew: Renew a user\'s verification status\n'
    '   Works same as $verify\n'
    '$unverify: Remove a user from verified seller status\n'
    '    Respond to a forwarded message of a user in private to unverify\n'
)
