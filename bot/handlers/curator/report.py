from pyrogram.handlers import MessageHandler
from pyrogram import filters
from django.conf import settings
from pyrogram.enums import ParseMode
from bot.utils.msg import (
    sched_cleanup
)
CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def handle_report(client, msg):
    if not msg.reply_to_message:
        msg.delete()
        return False

    target_msg = msg.reply_to_message
    from_user = msg.from_user
    target_user = msg.reply_to_message.from_user
    response = (
        f'{from_user.mention} reported a <a href="{target_msg.link}">message</a>'
        f' from {target_user.mention}'
    )
    client.send_message(
        chat_id=settings.REPORT_CHANNEL,
        text=response,
        parse_mode=ParseMode.HTML
    )
    notify = client.send_message(
        chat_id=msg.chat.id,
        text=response,
        parse_mode=ParseMode.HTML
    )
    sched_cleanup(msg)
    sched_cleanup(notify)


__HANDLERS__ = [
    MessageHandler(handle_report,
                   filters.command(['report', 'admin'], prefixes=CMD_PREFIX))
]

__HELP__ = (
    '$report/$admin: Report a message\n'
    '   Send $report as a reply to target message'
)
