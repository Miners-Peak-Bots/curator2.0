from pyrogram.handlers import MessageHandler
from pyrogram import filters
from group.models import Group
from django.conf import settings
from pyrogram.enums import ParseMode


__HELP__ = """Hey man
How is it going"""


def handle_notify(client, msg):
    print('report')
    if not msg.reply_to_message:
        msg.delete()
        return False

    from_user = msg.from_user
    target_user = msg.reply_to_message.from_user
    response = (
        f'{from_user.mention} reported a <a href="{msg.link}">message</a>'
        f' from {target_user.mention}'
    )
    client.send_message(
        chat_id=settings.REPORT_CHANNEL,
        text=response,
        parse_mode=ParseMode.HTML
    )


__HANDLERS__ = [
    MessageHandler(handle_notify,
                   filters.command('report', prefixes='!'))
]
