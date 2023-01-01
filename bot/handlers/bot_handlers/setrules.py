from pyrogram.handlers import MessageHandler
from pyrogram import filters
from django.conf import settings
from group.models import Group
CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def handle_set_rules(client, msg):
    if msg.from_user.id not in settings.BOT_MASTER:
        msg.delete()
        return False

    if not msg.reply_to_message:
        msg.delete()
        return False

    try:
        group = Group.objects.filter(pk=msg.chat.id).first()
    except Group.DoesNotExist:
        return msg.reply('Please run $updategroup first')

    prev_pin = group.rules_id
    target_msg = msg.reply_to_message
    pinmsg = client.copy_message(
        chat_id=msg.chat.id,
        from_chat_id=msg.chat.id,
        message_id=target_msg.id,
    )
    group.rules = target_msg.text
    group.rules_id = pinmsg.id
    group.save()
    pinmsg.pin()

    """
    delete previously pinned message message
    """
    if prev_pin:
        client.unpin_chat_message(
            chat_id=group.group_id,
            message_id=prev_pin
        )

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
