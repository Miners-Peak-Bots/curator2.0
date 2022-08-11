from pyrogram.handlers import MessageHandler
from user.models import TeleUser
from pyrogram import filters
from group.models import Group
from bot.utils.msg import (
    sched_cleanup
)


def handle_move(client, msg):
    if not msg.reply_to_message:
        msg.delete()
        return False

    if not len(msg.command) > 1:
        msg.delete()
        return False

    try:
        admin = TeleUser.objects.get(pk=msg.from_user.id)
    except TeleUser.DoesNotExist:
        reply = msg.reply_text('Admin not found')
        sched_cleanup(reply)
        return False

    if not admin.is_admin:
        msg.delete()
        return False

    target_msg = msg.reply_to_message
    target_group = msg.command[1]

    try:
        group = Group.objects.filter(shortname=target_group).get()
    except Group.DoesNotExist:
        msg.reply_text('Group not found')
        return False

    client.copy_message(
        chat_id=group.group_id,
        from_chat_id=msg.chat.id,
        message_id=target_msg.id,
    )
    target_msg.delete()
    msg.delete()


def handle_bulk_move(client, msg):
    if not msg.reply_to_message:
        msg.delete()
        return False

    if not len(msg.command) > 1:
        msg.delete()
        return False

    try:
        admin = TeleUser.objects.get(pk=msg.from_user.id)
    except TeleUser.DoesNotExist:
        reply = msg.reply_text('Admin not found')
        sched_cleanup(reply)
        return False

    if not admin.is_admin:
        msg.delete()
        return False

    target_msg = msg.reply_to_message
    target_group = msg.command[1]
    move_list = list(range(target_msg.id, msg.id))
    del_list = move_list + [msg.id]
    try:
        group = Group.objects.filter(shortname=target_group).get()
    except Group.DoesNotExist:
        reply = msg.reply_text('Group not found')
        sched_cleanup(reply)
        return False

    for msgid in move_list:
        client.copy_message(
            chat_id=group.group_id,
            from_chat_id=msg.chat.id,
            message_id=msgid,
        )

    client.delete_messages(
        chat_id=msg.chat.id,
        message_ids=del_list
    )


__HANDLERS__ = [
    MessageHandler(handle_move, filters.command('move', prefixes='!')),
    MessageHandler(handle_bulk_move, filters.command('bmove', prefixes='!')),
]


__HELP__ = (
    '!move: Move one to a specified destination\n'
    '   Destination group is identified by a shortname set in dashboard'
    '   Reply to a message with !move'
    '!bmove: Move more than one messages to a specified destination\n'
    '   Destination group is identified by a shortname set in dashboard'
    '   Reply to a message with !move'
    '   All succeeding messages will be moved as well'
)
