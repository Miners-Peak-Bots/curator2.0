from user.models import (
    TeleUser,
)
from user.utils import (
    ban_user
)
from group.models import Group
from bot.utils.user import (
    get_target_user,
    get_reason
)
from pyrogram.handlers import MessageHandler
from ...utils.msg import errorify, sched_cleanup
from pyrogram import filters
from pyrogram.enums import ParseMode
from bot.utils.msg import log
from django.conf import settings
CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def handle_ban(client, msg):
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
        reply = msg.reply_text('User could not be found')
        sched_cleanup(reply)
        return False

    try:
        reason = get_reason(msg)
    except Exception:
        reply = msg.reply_text('Please specify a reason to ban')
        sched_cleanup(reply)
        return False

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
    victim.log(message=reason, event=2)
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
        f'🚫 {msg.from_user.mention} banned {victim.mention}\n'
        f'<b>Reason:</b> {reason.strip()}\n'
    )
    log_msg = errorify(response, errors)
    log(client, log_msg)
    reply = client.send_message(msg.chat.id, response,
                                parse_mode=ParseMode.HTML)
    if msg.reply_to_message:
        """
        Delete the target message
        """
        msg.reply_to_message.delete()

    sched_cleanup(reply, interval=120)
    """
    Delete the command
    """
    msg.delete()


__HANDLERS__ = [
    MessageHandler(handle_ban, filters.command('ban', prefixes=CMD_PREFIX)),
]

__HELP__ADMIN__ = (
    '$ban: Ban a user from all the groups(admin only)\n'
    '    $ban 567319 Flooding chat\n'
    '    $ban @username Flooding chat\n'
    '    Reply to a user\'s message with $ban reason'
    '$unban: Unban a user from all the groups\n'
    '    $unban 567319 Flooding chat\n'
    '    $unban @username Flooding chat\n'
    '    Reply to a user\'s message with $unban'
)
