from .models import TeleUser
from datetime import datetime, timedelta
from pyrogram.types import ChatPermissions


def create_user(member):
    return TeleUser.objects.create(
        tele_id=member.id,
        username=member.username,
        first_name=member.first_name,
        last_name=member.last_name
    )


def create_get_user(member):
    return TeleUser.objects.get_or_create(
        tele_id=member.id,
        defaults={
            'username': member.username,
            'first_name': member.first_name,
            'last_name': member.last_name
        }
    )


def ban_user(client, user_id, chat_id):
    """
    This is a permanent ban since no `until_date` is specified
    """
    try:
        client.ban_chat_member(
            chat_id=chat_id,
            user_id=user_id
        )
    except Exception:
        raise


def unban_user(client, user_id, chat_id):
    try:
        client.unban_chat_member(
            chat_id=chat_id,
            user_id=user_id
        )
    except Exception:
        raise


def mute_user(client, chat_id, user_id, duration=30):
    until = datetime.now() + timedelta(days=duration)
    client.restrict_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        permissions=ChatPermissions(),
        until_date=until
    )
