from ..core.cache import Cache
from ..db.models import User
from ..db.pydantic_models import User as PyUser
from dataclasses import dataclass
import peewee


def load_users_cache():
    cache = Cache(PyUser)
    for user in User.select():
        cache.add(user.user_id, user)
    return cache


def get_user(user_id):
    try:
        user = User.get(User.user_id == user_id)
    except peewee.DoesNotExist:
        raise
    return user


def create_user(member, active=False):
    user = User(
        user_id=member.id,
        username=member.username,
        first_name=member.first_name,
        last_name=member.last_name,
        active=active
    )
    user.save(force_insert=1)
    return user


def is_admin(client, user):
    if user.user_id == client.config.general.master_id:
        return True

    return user.admin
