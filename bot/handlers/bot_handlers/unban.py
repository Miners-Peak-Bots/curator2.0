from user.models import (
    TeleUser,
)
from user.utils import (
    create_get_user,
    ban_user
)
# from djang.conf import settings
from group.models import Group
from pyrogram.handlers import MessageHandler
from ...utils.msg import errorify
from pyrogram import filters


def handle_ban(client, msg):
    if not msg.reply_to_message:
        msg.delete()
        return False

    if not len(msg.command) > 1:
        """
        A warn reason was not provided
        """
        msg.delete()
        return False

    try:
        admin = TeleUser.objects.get(pk=msg.from_user.id)
    except TeleUser.DoesNotExist:
        msg.reply_text('Admin not found')
        return False

    target_user = msg.reply_to_message.from_user
    victim, created = create_get_user(target_user)
    reason = msg.text.replace('!ban', '').strip()

    if not admin.is_admin:
        msg.delete()
        return False

    if victim.is_admin:
        msg.delete()
        return False

    victim.banned = True
    victim.save()
    warn = victim.warn(
        banning_warn=True,
        reason=reason,
        admin=admin,
    )
    print(warn.reason, warn.id)
    errors = []
    for group in Group.objects.all():
        try:
            ban_user(
                client=client,
                user_id=victim.tele_id,
                chat_id=group.group_id
            )
        except Exception as e:
            errors.append(
                f'Could not ban {victim.tele_id} '
                f'on chat {group.group_id} due to '
                f'{str(e)}')

    response = (
        f'{msg.from_user.mention} banned {target_user.mention} for\n'
        f'<code>{reason}</code>\n'
    )
    response = errorify(response, errors)
    client.send_message(msg.chat.id, response, parse_mode='html')


__HANDLERS__ = [
    MessageHandler(handle_ban, filters.command('unban', prefixes='!')),
]

__HELP__ = ''
