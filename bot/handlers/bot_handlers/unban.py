from user.models import (
    TeleUser,
)
from user.utils import (
    unban_user
)
from group.models import Group
from pyrogram.handlers import MessageHandler
from ...utils.msg import errorify
from pyrogram import filters
from bot.utils.user import get_target_user
from pyrogram.enums import ParseMode
from bot.utils.msg import log


def handle_unban(client, msg):
    try:
        admin = TeleUser.objects.get(pk=msg.from_user.id)
    except TeleUser.DoesNotExist:
        msg.reply_text('Admin not found')
        return False

    try:
        victim = get_target_user(msg)
        print(victim)
    except Exception:
        return msg.reply_text('User not found')

    if not admin.is_admin:
        msg.delete()
        return False

    if victim.is_admin:
        msg.delete()
        return False

    victim.banned = False
    victim.save()
    errors = []
    for group in Group.objects.all():
        try:
            unban_user(
                client=client,
                user_id=victim.tele_id,
                chat_id=group.group_id
            )
        except Exception as e:
            errors.append(
                f'Could not unban {victim.tele_id} '
                f'on chat {group.group_id} due to '
                f'{str(e)}')

    response = (
        f'{msg.from_user.mention} unbanned {victim.mention}'
    )
    logmsg = errorify(response, errors)
    log(client, logmsg)
    client.send_message(msg.chat.id, response, parse_mode=ParseMode.HTML)


__HANDLERS__ = [
    MessageHandler(handle_unban, filters.command('unban', prefixes='!')),
]

__HELP__ = (
    '!unban: Unban a user from all the groups(admin only)\n'
    '    !unban 567319 Flooding chat\n'
    '    !unban @username Flooding chat\n'
    '    Reply to a user\'s message with !unban'
)
