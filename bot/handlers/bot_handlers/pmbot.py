from user.models import (
    TeleUser,
)

from group.models import Group

from pyrogram.handlers import ChatJoinRequestHandler, CallbackQueryHandler, MessageHandler


from pyrogram import Client, filters

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from django.conf import settings

CMD_PREFIX = settings.BOT_COMMAND_PREFIX


# def set_group_rule(client, message):
#     if message.from_user.id not in settings.BOT_MASTER:
#         message.delete()
#         return False

#     try:
#         data = message.text.split()
#         group = client.get_chat(data[1])
#         rule = data[2]
#     except IndexError:
#         message.reply("You should set group and rule")
#         message.reply(f"`{CMD_PREFIX}set_rule group rule`")
#         return False
#     except Exception as e:
#         message.reply(e)
#         return False

#     if Group.objects.filter(group_id=group.id, vendor=True):
#         Group.objects.filter(group_id=group.id, vendor=True).update(group_rule=rule)
#         message.reply("Done")
#     else:
#         message.reply("add group to special group")


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

    client.send_message(
        chat_id=msg.from_user.id,
        text=group.rules,
        reply_markup=keyboard
    )


def group_rules_callback(client, callback_query):
    data = callback_query.data.split()
    user_id = callback_query.from_user.id
    group_id = int(data[1])
    callback_query.answer(text="Congrats your request to join group has been accepted", show_alert=True)
    client.approve_chat_join_request(group_id, user_id)
    callback_query.message.edit_reply_markup(
        reply_markup=None,
    )


__HANDLERS__ = [
    # MessageHandler(set_group_rule, filters.command('set_rule', prefixes=CMD_PREFIX)),
    ChatJoinRequestHandler(group_rules_pm),
    CallbackQueryHandler(group_rules_callback, filters.regex("^unmute\s-?[0-9]+$")),
]
