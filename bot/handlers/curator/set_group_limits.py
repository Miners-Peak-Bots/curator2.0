from django.conf import settings
from pyrogram import filters
from pyrogram.handlers import MessageHandler

from group.models import Group, GroupLimits

CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def set_limits(client, msg):
    if msg.from_user.id not in settings.BOT_MASTER:
        msg.delete()
        return False

    group_id = msg.chat.id

    try:
        group = Group.objects.get(group_id=group_id)
    except Group.DoesNotExist:
        msg.reply("This group isnt managed by curator.")
        return None
    else:
        message_text_list = msg.text.split()

        if len(message_text_list) != 3:
            return msg.reply_text('Invalid command format. Use $setlimits word_limit new_line_limit')

        try:
            word_limit = int(message_text_list[1]) if message_text_list[1] != 'null' else None
            new_line_limit = int(message_text_list[2]) if message_text_list[2] != 'null' else None
        except ValueError:
            return msg.reply_text('word_limit and new_line_limit should be null or an integer value')

        GroupLimits.objects.update_or_create(
            group=group, defaults={"word_limit": word_limit, "new_line_limit": new_line_limit}
        )

        msg.reply_text(
            f"Word limit and new line limit of group {msg.chat.title} set to {word_limit} and {new_line_limit} respectively."
        )


__HANDLERS__ = [
    MessageHandler(set_limits, (filters.command('setlimits', prefixes=CMD_PREFIX) & filters.group)),
]


__HELP__ADMIN__ = '$setlimits word_limit new_line_limit: Set word limit and new line limit for group, $setlimits null null disable limits\n'
