from .models import TeleUser


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
