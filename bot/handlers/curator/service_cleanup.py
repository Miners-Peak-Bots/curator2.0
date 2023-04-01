from pyrogram.handlers import (
    MessageHandler,
    RawUpdateHandler
)
from pyrogram import filters
from pyrogram.raw import types


def cleanup_servicemsg(client, msg):
    msg.delete()


def handle_raw(client, update, users, chats):
    """
    This bit of code is to remove service message that is delivered
    when user is approved into a group after completing captcha
    """
    print(update)
    action = types.MessageActionChatJoinedByRequest
    try:
        if isinstance(update.message.action, action):
            channel_id = update.message.peer_id.channel_id

            msg_id = update.message.id
            chat_id = f'-100{channel_id}'

            client.delete_messages(
                chat_id=chat_id,
                message_ids=msg_id
            )
    except Exception:
        pass

    return True


__HANDLERS__ = [
    MessageHandler(cleanup_servicemsg, filters.service),
    RawUpdateHandler(handle_raw)
]
