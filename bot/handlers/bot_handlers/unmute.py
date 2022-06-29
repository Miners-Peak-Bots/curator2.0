from pyrogram.types import ChatPermissions
from user.utils import create_get_user
from pyrogram.handlers import CallbackQueryHandler
from pyrogram import filters


def handle_unmute(client, msg):
    from_user = msg.from_user
    user, created = create_get_user(from_user)
    if user.active:
        msg.answer('You are already unmuted')
        return False

    try:
        client.restrict_chat_member(
            msg.message.chat.id,
            from_user.id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_send_polls=True,
                can_add_web_page_previews=True,
                can_invite_users=True,
                can_pin_messages=False,
                can_change_info=False,
            ),
        )
        user.active = True
        user.save()
        msg.answer('You have been unmuted')
    except Exception:
        msg.answer('You are an admin or already unmuted', True)


__HANDLERS__ = [
    CallbackQueryHandler(handle_unmute, filters.regex('unmute'))
]

__HELP__ = ''
