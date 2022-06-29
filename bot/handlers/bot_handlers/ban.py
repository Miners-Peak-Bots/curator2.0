from user.models import (
    TeleUser,
)
from user.utils import (
    ban_user
)
from group.models import Group
from bot.utils.user import get_target_user_and_reason
from pyrogram.handlers import MessageHandler
from ...utils.msg import errorify
from pyrogram import filters
from pyrogram.enums import ParseMode


def handle_ban(client, msg):
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

    try:
        data = get_target_user_and_reason(msg, ommit='!ban')
    except Exception:
        return msg.reply_text('User not found')

    victim = data['user']
    reason = data['reason']

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
        f'{msg.from_user.mention} banned {victim.mention} for\n'
        f'<code>{reason}</code>\n'
    )
    response = errorify(response, errors)
    client.send_message(msg.chat.id, response, parse_mode=ParseMode.HTML)


__HANDLERS__ = [
    MessageHandler(handle_ban, filters.command('ban', prefixes='!')),
]

__HELP__ = ''
