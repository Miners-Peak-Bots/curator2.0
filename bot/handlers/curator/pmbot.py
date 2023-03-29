from group.models import Group
from pyrogram.handlers import ChatJoinRequestHandler, CallbackQueryHandler
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.conf import settings
from captcha.models import Captcha
from captcha.lib import CaptchaEngine

CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def group_rules_pm(client, msg):
    try:
        group = Group.objects.filter(pk=msg.chat.id).first()
    except Exception:
        return False

    group_id = group.group_id
    keyboard = InlineKeyboardMarkup(
             [
                 [
                     InlineKeyboardButton("Okay! Unmute me",
                                          callback_data=f"unmute {group_id}"),
                 ]
             ]
         )

    client.copy_message(
        chat_id=msg.from_user.id,
        from_chat_id=group.group_id,
        message_id=group.rules_id,
        # reply_markup=keyboard
    )
    captcha = CaptchaEngine()
    try:
        captcha_db = Captcha.objects.create(answer=captcha.ans,
                                            group_id=msg.chat.id)
    except Exception as e:
        print(str(e))
        client.send_message(
            msg.from_user.id,
            text='An unexpected error occured. Please report to admin'
        )
        raise
        return False

    if msg.chat.username:
        chatusername = f'@{msg.chat.username}'
    else:
        chatusername = msg.chat.title

    client.send_message(
        chat_id=msg.from_user.id,
        text=f'Please read me to join {chatusername}',
        reply_markup=captcha.keyboard(captcha_db.id)
    )


# def group_rules_callback(client, callback_query):
#     data = callback_query.data.split('_')
#     user_id = callback_query.from_user.id
#     group_id = int(data[1])
#     callback_query.answer(text="Congrats your request to join group has been accepted", show_alert=True)
#     client.approve_chat_join_request(group_id, user_id)
#     callback_query.message.edit_reply_markup(
#         reply_markup=None,
#     )


__HANDLERS__ = [
    # MessageHandler(set_group_rule, filters.command('set_rule', prefixes=CMD_PREFIX)),
    ChatJoinRequestHandler(group_rules_pm),
    # CallbackQueryHandler(group_rules_callback, filters.regex("^unmute\s-?[0-9]+$")),
]
