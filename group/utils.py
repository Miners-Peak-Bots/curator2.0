from .models import Group


def create_get_group(chat):
    return Group.objects.get_or_create(
        group_id=chat.id,
        defaults={
            'title': chat.title,
            'enabled': True
        }
    )
