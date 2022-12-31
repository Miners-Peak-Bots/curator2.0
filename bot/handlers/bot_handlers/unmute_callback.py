from pyrogram.handlers import CallbackQueryHandler
from pyrogram import filters
from group.models import Group

### DEPRECATED

def handle_unmute_callback(client, msg):
    from_user = msg.from_user
    chat = msg.message.chat

    try:
        group = Group.objects.get(pk=chat.id)
    except Exception as e:
        repr(e)
        msg.answer('An unexpected error ocucred. Please talk to an admin')
        return False

    try:
        client.restrict_chat_member(
            chat_id=group.group_id,
            user_id=from_user.id,
            permissions=group.get_permissions()
        )
    except Exception as e:
        repr(e)
        msg.answer('An unexpected error ocucred. Please talk to an admin')
        return False

    msg.answer('You have been unmuted')


__HANDLERS__ = [
    # CallbackQueryHandler(handle_unmute_callback, filters.regex('unmute'))
]
