from user.utils import (
    prep_acheck,
    prep_check
)
from pyrogram.handlers import MessageHandler
from pyrogram import filters
from pyrogram.enums import ParseMode
from user.models import (
    TeleUser
)


def pm_check(client, msg):
    if msg.forward_sender_name:
        return msg.reply_text(f'{msg.forward_sender_name} has forward privacy enabled')
    elif msg.forward_from:
        target = msg.forward_from

        try:
            user = TeleUser.objects.get(pk=target.id)
        except TeleUser.DoesNotExist:
            user = TeleUser.objects.create(
                tele_id=target.id,
                first_name=target.first_name,
                last_name=target.last_name,
                username=target.username
            )

        """
        update details of the user
        """
        user.first_name = target.first_name
        user.last_name = target.last_name
        user.username = target.username
        user.save()
        try:
            current_user = TeleUser.objects.get(pk=msg.from_user.id)
        except TeleUser.DoesNotExist:
            return msg.reply('You do not have the rights to run this operation')

        if current_user.is_admin:
            response = prep_acheck(user)
        else:
            response = prep_check(user)

        return client.send_message(
            chat_id=msg.from_user.id,
            text=response,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    else:
        msg.reply('Unknown error occured, could not find user')


__HANDLERS__ = [
    MessageHandler(pm_check, (filters.forwarded & filters.private)),
]
