from user.models import (
    TeleUser
)
from bot.utils.user import (
    get_target_user,
    get_reason
)
from bot.utils.msg import (
    sched_cleanup
)
from pyrogram.handlers import MessageHandler
from pyrogram import filters
from pyrogram.enums import ParseMode
from user.utils import ban_user, mute_user
from django.conf import settings
CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def handle_warn(client, msg):
    if not len(msg.command) > 1:
        """
        A warn reason was not provided
        """
        reply = msg.reply_text('Please specify a reason')
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
        reply = msg.reply_text('Please specify a reason')
        sched_cleanup(reply)
        return False

    if not admin.is_admin:
        msg.delete()
        return False

    if victim.is_admin:
        msg.delete()
        return False

    warn = victim.warn(
        admin=admin,
        reason=reason
    )
    warn.save()
    warnings = victim.warning.count()
    response = (
        f'⚠️ {msg.from_user.mention} warned {victim.mention} for\n'
        f'<b>Reason:</b> {reason.strip()}</code>\n'
        f'Warn {victim.warning.count()}/5\n'
        # f'Warn {warns}/3'
    )
    if warnings == 3:
        print("muting for 30")
        """
        Mute for 30 days
        """
        mute_user(client, msg.chat.id, victim.tele_id, 30)
        victim.log(message=reason, event=4)
        response = response + 'User has been muted for 30 days'

    elif warnings == 4:
        print("muting for 60")
        """
        Mute for 60 days
        """
        mute_user(client, msg.chat.id, victim.tele_id, 60)
        victim.log(message=reason, event=4)
        response = response + 'User has been muted for 60 days'

    elif warnings == 5:
        """
        Ban the user
        """
        ban_user(msg.chat, victim, client)
        warn.banning_warn = True
        warn.save()
        victim.banned = True
        victim.save()
        victim.log(message=reason, event=2)
        response = response + 'User has been banned'
    else:
        victim.log(message=reason, event=0)

    reply = client.send_message(msg.chat.id, response,
                                parse_mode=ParseMode.HTML)
    sched_cleanup(reply)
    if msg.reply_to_message:
        """
        Delete the target message
        """
        # msg.reply_to_message.delete()
        sched_cleanup(msg.reply_to_message, interval=120)

    """
    Delete the issued command
    """
    msg.delete()
    sched_cleanup(msg, interval=120)


__HANDLERS__ = [
    MessageHandler(handle_warn, filters.command('warn', prefixes=CMD_PREFIX)),
]

__HELP__ADMIN__ = (
    '$warn: warn a user(admin only)\n'
    '    $warn 567319 Flooding chat\n'
    '    $warn @username Flooding chat\n'
    '    Reply to a user\'s message with $warn reason'
)
