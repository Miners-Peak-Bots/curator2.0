from .models import Group
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_get_group(chat):
    return Group.objects.get_or_create(
        group_id=chat.id,
        defaults={
            'title': chat.title,
            'enabled': True
        }
    )


def prepare_move_message(message):
    text = message.text
    group = message.chat
    return (
        f'<b>This message was moved to </b> <i>{group.title}</i>\n'
        f'<code>{text}</code>'
    )


def prepare_follow_move_kb(message):
    reply_markup = [
        [
            InlineKeyboardButton('Continue', url=message.link)
        ]
    ]
    return InlineKeyboardMarkup(reply_markup)
