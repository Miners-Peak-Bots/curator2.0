from ..db.models import Group
from ..db.pydantic_models import Group as PyGroup
from ..core.cache import Cache
import peewee


def load_groups_cache():
    group_cache = Cache(PyGroup)
    for group in Group.select():
        group_cache.add(group.group_id, group)
    return group_cache


def get_group(group_id):
    try:
        group = Group.get(Group.group_id == group_id)
    except peewee.DoesNotExist:
        raise
    return group


def parse_entities(msg):
    """
    Iterates Message.entities and prepares
    an array of objects that can later be
    easily worked with for identifying forbidden
    chats, links etc.
    """
    if not msg.entities:
        return []
    parsed = []
    text = msg.text
    for entity in msg.entities:
        offset = entity.offset
        length = entity.length
        msg_text = text[offset:(offset+length)]
        parsed.append(
            {
                'token': msg_text,
                'token_type': entity.type
            }
        )
    return parsed
