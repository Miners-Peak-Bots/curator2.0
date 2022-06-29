from user.models import (
    TeleUser
)
from bot.utils.user import get_target_user_and_reason
from pyrogram.handlers import MessageHandler
from pyrogram import filters
from pyrogram.enums import ParseMode


def handle_warn(client, msg):
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
        data = get_target_user_and_reason(msg)
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

    warn = victim.warn(
        admin=admin,
        reason=reason
    )
    warn.save()

    response = (
        f'⚠️ {msg.from_user.mention} warned {victim.mention} for\n'
        f'<b>Reason:</b> {reason.strip()}</code>\n'
        # f'Warn {warns}/3'
    )
    client.send_message(msg.chat.id, response, parse_mode=ParseMode.HTML)
    if msg.reply_to_message:
        msg.reply_to_message.delete()


__HANDLERS__ = [
    MessageHandler(handle_warn, filters.command('warn', prefixes='!')),
]

__HELP__ = ''
