from django.conf import settings
from pyrogram import filters
from pyrogram.handlers import MessageHandler

from group.models import Group, GroupLimits
from pyrogram import Client
from django.core.exceptions import ObjectDoesNotExist
from bot.utils.msg import sched_cleanup

CMD_PREFIX = settings.BOT_COMMAND_PREFIX


@Client.on_message(filters.incoming & filters.group, group=-1)
def limit_check(client, msg):
    try:
        if msg.from_user.id in settings.BOT_MASTER:
            return None

        text = msg.text or msg.caption

        if text is None:
            return None

        group_id = msg.chat.id

        try:
            group_limits = Group.objects.get(group_id=group_id).group_limits
        except ObjectDoesNotExist:
            return None

        user_id = msg.from_user.id

        if user_id is None:
            return None

        character_limit = group_limits.character_limit
        new_line_limit = group_limits.new_line_limit

        if (character_limit is not None and len(text) > character_limit) or (
            new_line_limit is not None and (text.count("\n") + 1) > new_line_limit
        ):
            msg.delete()

            sent = client.send_message(
                group_id,
                text=f"Hi {msg.from_user.mention}, Make sure your message doesnt contain more than {character_limit} characters(including spaces) and {new_line_limit} lines.",
            )

            sched_cleanup(msg=sent, interval=10)

        return None

    finally:
        msg.continue_propagation()


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
            return msg.reply_text(
                "Invalid command format. Use $setlimits character_limit new_line_limit"
            )

        try:
            character_limit = (
                int(message_text_list[1]) if message_text_list[1] != "null" else None
            )
            new_line_limit = (
                int(message_text_list[2]) if message_text_list[2] != "null" else None
            )
        except ValueError:
            return msg.reply_text(
                "character_limit and new_line_limit should be null or an integer value"
            )

        GroupLimits.objects.update_or_create(
            group=group,
            defaults={
                "character_limit": character_limit,
                "new_line_limit": new_line_limit,
            },
        )

        msg.reply_text(
            f"character_limit and new_line_limit of group {msg.chat.title} set to {character_limit} and {new_line_limit} respectively."
        )


__HANDLERS__ = [
    MessageHandler(
        set_limits, (filters.command("setlimits", prefixes=CMD_PREFIX) & filters.group)
    ),
]


__HELP__ADMIN__ = "$setlimits character_limit new_line_limit: Set character limit and new line limit for group, $setlimits null null disable limits\n"
