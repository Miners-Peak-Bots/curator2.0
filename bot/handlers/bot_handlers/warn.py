from user.models import (
    TeleUser
)
from bot.utils.user import (
    get_target_user,
    get_reason
)
from pyrogram.handlers import MessageHandler
from pyrogram import filters
from pyrogram.enums import ParseMode
from user.utils import ban_user, mute_user


def handle_warn(client, msg):
    if not len(msg.command) > 1:
        """
        A warn reason was not provided
        """
        msg.reply_text('Please specify a reason to warn for')
        return False

    try:
        admin = TeleUser.objects.get(pk=msg.from_user.id)
    except TeleUser.DoesNotExist:
        msg.reply_text('Admin not found')
        return False

    try:
        victim = get_target_user(msg)
    except Exception:
        return msg.reply_text('User could not be found')

    try:
        reason = get_reason(msg)
    except Exception:
        return msg.reply_text('Please specify a reason to warn')

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
        # f'Warn {warns}/3'
    )
    if warnings == 3:
        print("muting for 30")
        """
        Mute for 30 days
        """
        mute_user(client, msg.chat.id, victim.tele_id, 30)
        response = response + 'User has been muted for 30 days'

    if warnings == 6:
        print("muting for 90")
        """
        Mute for 60 days
        """
        mute_user(client, msg.chat.id, victim.tele_id, 60)
        response = response + 'User has been muted for 60 days'

    if warnings == 9:
        """
        Ban the user
        """
        ban_user(msg.chat, victim, client)
        warn.banning_warn = True
        warn.save()
        victim.banned = True
        victim.save()
        response = response + 'User has been banned'

    client.send_message(msg.chat.id, response, parse_mode=ParseMode.HTML)
    if msg.reply_to_message:
        """
        Delete the target message
        """
        msg.reply_to_message.delete()

    """
    Delete the issued command
    """
    msg.delete()


__HANDLERS__ = [
    MessageHandler(handle_warn, filters.command('warn', prefixes='!')),
]

__HELP__ = (
    '!warn: warn a user(admin only)\n'
    '    !warn 567319 Flooding chat\n'
    '    !warn @username Flooding chat\n'
    '    Reply to a user\'s message with !warn reason'
)
