from pyrogram.handlers import MessageHandler
from pykeyboard import InlineKeyboard, InlineButton
from pyrogram import filters
from django.conf import settings
CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def handle_set_rules(client, msg):
    if msg.from_user.id not in settings.BOT_MASTER:
        msg.delete()
        return False

    if not msg.reply_to_message:
        msg.delete()
        return False

    target_msg = msg.reply_to_message
    # rules = target_msg.text
    keyboard = InlineKeyboard(row_width=1)
    keyboard.add(
        InlineButton('Okay! Unmute me', 'unmute'),
    )
    # msg = await client.send_message(msg.chat.id, rules,
    #                                 reply_markup=keyboard,
    #                                 parse_mode='markdown')
    pinmsg = client.copy_message(
        chat_id=msg.chat.id,
        from_chat_id=msg.chat.id,
        message_id=target_msg.id,
        reply_markup=keyboard
    )
    pinmsg.pin()
    msg.delete()
    target_msg.delete()


__HANDLERS__ = [
    MessageHandler(handle_set_rules, (
        filters.command('setrules', prefixes=CMD_PREFIX)
        &
        filters.group
    ))
]


__HELP__ADMIN__ = (
    '$setrules: Set a rules message and attach unmute button\n'
    '    Reply to a message with $setrules to pin and set it as rules'
)
