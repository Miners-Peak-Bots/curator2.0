from pyrogram.handlers import MessageHandler
from pyrogram import filters
from pyrogram.raw import types
from pyrogram import Client, filters
from pyrogram import ContinuePropagation


def cleanup_servicemsg(client, msg):
    msg.delete()


@Client.on_raw_update(group=-1)
def handle_raw(client, update, users, chats):
    """
    This bit of code is to remove service message that is delivered
    when user is approved into a group after completing captcha
    """
    # print(client, update, users, chats)

    try:
        action = types.MessageActionChatJoinedByRequest
        if isinstance(update.message.action, action):
            channel_id = update.message.peer_id.channel_id

            msg_id = update.message.id
            chat_id = f'-100{channel_id}'

            client.delete_messages(chat_id=chat_id, message_ids=msg_id)
    except Exception:
        pass
    finally:
        raise ContinuePropagation


__HANDLERS__ = [
    MessageHandler(cleanup_servicemsg, filters.service),
]
