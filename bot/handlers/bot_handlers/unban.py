from user.models import (
    TeleUser,
)
from user.utils import (
    unban_user
)
from group.models import Group
from pyrogram.handlers import MessageHandler
from ...utils.msg import errorify, sched_cleanup
from pyrogram import filters
from bot.utils.user import (
    get_target_user,
    get_reason
)
from pyrogram.enums import ParseMode
from bot.utils.msg import log
from django.conf import settings
CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def handle_unban(client, msg):
    if not len(msg.command) > 1:
        """
        A warn reason was not provided
        """
        reply = msg.reply_text('Please specify a reason to warn for')
        sched_cleanup(reply)
        return False

    try:
        admin = TeleUser.objects.get(pk=msg.from_user.id)
    except TeleUser.DoesNotExist:
        reply = msg.reply_text('Admin not found')
        sched_cleanup(reply)
        return False

    try:
        victim = get_target_user(msg)
    except Exception:
        reply = msg.reply_text('User not found')
        sched_cleanup(reply)

    try:
        reason = get_reason(msg)
    except Exception:
        reply = msg.reply_text('Please specify a reason to unban')
        sched_cleanup(reply)
        return False

    if not admin.is_admin:
        msg.delete()
        return False

    if victim.is_admin:
        msg.delete()
        return False

    victim.banned = False
    victim.save()
    victim.log(message=reason, event=3)
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
                f'on chat {group.title}({group.id}) due to '
                f'{str(e)}')

    response = (
        f'{msg.from_user.mention} unbanned {victim.mention}'
    )
    logmsg = errorify(response, errors)
    log(client, logmsg)
    client.send_message(msg.chat.id, response, parse_mode=ParseMode.HTML)


__HANDLERS__ = [
    MessageHandler(handle_unban,
                   filters.command('unban', prefixes=CMD_PREFIX)),
]

__HELP__ADMIN__ = (
    '$unban: Unban a user from all the groups(admin only)\n'
    '    $unban 567319 Flooding chat\n'
    '    $unban @username Flooding chat\n'
    '    Reply to a user\'s message with $unban'
)
