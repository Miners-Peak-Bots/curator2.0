from user.models import (
    TeleUser
)
from bot.utils.msg import (
    sched_cleanup
)
from bot.utils.user import (
    get_target_user,
    get_reason
)
from pyrogram.handlers import MessageHandler
from pyrogram import filters
from pyrogram.enums import ParseMode
from django.conf.settings import (
    BOT_COMMAND_PREFIX as CMD_PREFIX
)


def handle_unwarn(client, msg):
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
        return False

    try:
        reason = get_reason(msg)
    except Exception:
        reply = msg.reply_text('Please specify a reason to unwarn')
        sched_cleanup(reply)
        return False

    if not admin.is_admin:
        msg.delete()
        return False

    if victim.is_admin:
        msg.delete()
        return False

    if not victim.warning.count():
        msg.delete()
        return False

    warning = victim.warning.last()
    warning.delete()
    victim.log(message=reason, event=1)
    response = (
        f'❎ {msg.from_user.mention} pardoned {victim.mention} for\n'
        f'<b>Reason:</b> {warning.reason.strip()}\n'
        f'<b>Warns:</b> {victim.warning.count()}/5'
    )
    reply = client.send_message(msg.chat.id, response,
                                parse_mode=ParseMode.HTML)
    sched_cleanup(reply)
    msg.delete()


__HANDLERS__ = [
    MessageHandler(handle_unwarn,
                   filters.command('unwarn', prefixes=CMD_PREFIX)),
]

__HELP__ADMIN__ = (
    "$unwarn: Remove a user's latest warn(admin only)"
    '    $unwarn 567319\n'
    '    $unwarn @username\n'
    '    Reply to a user\'s message with $unwarn'
)
