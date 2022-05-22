from user.models import (
    TeleUser
)
from user.utils import create_get_user
from pyrogram.handlers import MessageHandler
from pyrogram import filters


def handle_warn(client, msg):
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

    if not admin.is_admin:
        msg.delete()
        return False

    if victim.is_admin:
        msg.delete()
        return False

    reason = msg.text.replace('!warn', '').strip()
    warn = victim.warn(
        admin=admin,
        reason=reason
    )
    warn.save()

    response = (
        f'{msg.from_user.mention} warned {target_user.mention} for\n'
        f'<code>{reason}</code>\n'
        # f'Warn {warns}/3'
    )
    client.send_message(msg.chat.id, response, parse_mode='html')


__HANDLERS__ = [
    MessageHandler(handle_warn, filters.command('warn', prefixes='!')),
]

__HELP__ = ''
