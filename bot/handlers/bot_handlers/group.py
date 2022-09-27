# from ...utils.user import get_user, create_user
from ...utils.group import parse_entities
from group.utils import create_get_group
from user.utils import create_get_user
from pyrogram.handlers import MessageHandler
from pyrogram import filters
from django.conf import settings
from group.models import Group
from user.models import TeleUser


__HELP__ = ''


def acronym(orig_word):
    words = orig_word.split()
    if len(words) > 1:
        """
        Group title has whitespace in them
        eg: Foobar Group
        """
        letters = [word[0].upper() for word in words]
    else:
        """
        Group title does not have whitespace in them
        eg: FooBarGroup
        """
        letters = [
            letter if letter.isupper() else None for letter in orig_word
        ]
        letters = [letter for letter in letters if letter is not None]

        if len(letters) == 0:
            """
            Cmon all of its in lowercase?

            This needs a better solution
            """
            return f'{orig_word[0:3]}{orig_word[0:3]}'

    return ''.join(letters)


def handle_new_user(client, msg):
    """
    A user joined the group
    """
    for member in msg.new_chat_members:
        user, created = TeleUser.objects.get_or_create(
            tele_id=member.id,
            username=member.username,
            first_name=member.first_name,
            last_name=member.last_name
        )


def handle_self_add(client, msg):
    """
    The bot was added to a group.
    """
    if msg.from_user.id != settings.BOT_MASTER:
        client.send_message(msg.chat.id, "Oops! I don't belong here")
        client.leave_chat(msg.chat.id)

    """
    Add group to database
    """
    group, created = Group.objects.get_or_create(
        group_id=msg.chat.id,
        enabled=True,
        title=msg.chat.title,
        shortname=acronym(msg.chat.title)
    )
    response = (
        f"Great! I'll help manage the group.\n"
        f"Group short tag is {group.shortname}"
    )
    client.send_message(
        msg.chat.id,
        response
    )


def handle_group_join(client, msg):
    if client.me.id == msg.new_chat_members[0].id:
        """
        The bot was added to a group. Add group to list of groups.
        Leave if not added by master admin.
        """
        handle_self_add(client, msg)
        return

    """
    A user joined the group
    """
    handle_new_user(client, msg)


def handle_messages(client, msg):
    """
    Check if user is banned, if so ban him.
    Since curator is a multi group administration bot, a new group might
    be added after a user is banned. This means the user will not be banned in
    said group, so the ban has to be issued in the new group.
    """
    if msg.sender_chat:
        """
        User is sending messages as channel/group
        delete the message and stop processing
        """
        msg.delete()
        return False

    user, created = create_get_user(msg.from_user)
    if user.banned:
        msg.delete()
        print('user is banned. reapply')

    group, created_grp = create_get_group(msg.chat)
    if group.log_channel:
        msg.forward(group.log_channel)

    entities = parse_entities(msg)
    msg.continue_propagation()


def handle_group_update(client, msg):
    group, created = create_get_group(msg.chat)
    group.username = msg.chat.username
    group.title = msg.chat.title
    if not group.shortname:
        group.shortname = acronym(group.title)
    group.save()
    response = (
        f'Group updated\n'
        f'Group short tag is {group.shortname}'
    )
    client.send_message(msg.chat.id,
                        response)


def handle_id(client, msg):
    client.send_message(msg.chat.id, msg.chat.id)


__HANDLERS__ = [
    MessageHandler(handle_id, filters.command('id', prefixes='!')),
    MessageHandler(handle_group_join, filters.new_chat_members),
    MessageHandler(handle_messages, (filters.all & filters.group)),
    MessageHandler(handle_group_update,
                   (filters.command('updategroup', prefixes='!') &
                    filters.group))
]
