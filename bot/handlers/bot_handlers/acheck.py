from ...utils.msg import titlefy, linkify, titlefy_simple, boldify
from pyrogram.handlers import MessageHandler
import emoji
from pyrogram.enums import ParseMode
from pyrogram import filters
from user.utils import create_get_user
from bot.utils.user import get_target_user
from bot.utils.msg import (
    sched_cleanup
)
from user.utils import (
    prep_acheck
)
from django.conf import settings
CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def handle_acheck(client, msg):
    admin, created = create_get_user(msg.from_user)
    if not admin.is_admin:
        msg.delete()
        return False

    try:
        member = get_target_user(msg)
    except Exception:
        reply = msg.reply_text('User not found')
        sched_cleanup(reply)
        return False

    response = prep_acheck(member)
    reply = client.send_message(
        chat_id=admin.tele_id,
        text=response,
        disable_web_page_preview=True,
        parse_mode=ParseMode.HTML
    )
    sched_cleanup(reply)


__HANDLERS__ = [
    MessageHandler(handle_acheck,
                   filters.command('acheck', prefixes=CMD_PREFIX)),
]


__HELP__ADMIN__ = (
    "$acheck: Check a user's status(admin only)"
    '    $acheck 5431231\n'
    '    $acheck @username\n'
    '    Reply to a user\'s message with $acheck'
)
