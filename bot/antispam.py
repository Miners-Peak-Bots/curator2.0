from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from pyrogram import Client, filters, idle
from pyrogram.enums import ChatType

from bot.utils.msg import log
from bot.utils.msg import sched_cleanup

from group.models import Group
from user.models import TeleUser

api_id = settings.BOT_API_ID
api_hash = settings.BOT_API_HASH
token = settings.ANTISPAM_BOT_TOKEN

app = Client('antispam.bot', api_id=api_id, api_hash=api_hash, bot_token=token)

msgcount = {}


def get_admins():
    admins_all = TeleUser.objects.filter(admin=True).values_list('tele_id')
    admins = [admin[0] for admin in admins_all]
    admins.extend(settings.BOT_MASTER)
    return admins


def is_admin(user_id):
    return user_id in get_admins()


@app.on_message(filters.regex('.+[\u4E00-\uA000]'))
def handle_msg(client, msg):
    msg.delete()


@app.on_message(filters.regex('.+[\u0600-\u06ff]'))
def handle_msg2(client, msg):
    msg.delete()


@app.on_message(filters.regex('(https?:\/\/)?(www[.])?(telegram|t)\.me\/([a-zA-Z0-9_-]*)\/?$'))
def handle_msg3(client, msg):
    msg.delete()


@app.on_message(filters.text & filters.group)
def handle_msg4(client, msg):
    try:
        user = TeleUser.objects.get(pk=msg.from_user.id)
    except TeleUser.DoesNotExist:
        user = TeleUser.objects.create(
            tele_id=msg.from_user.id,
            first_name=msg.from_user.first_name,
            last_name=msg.from_user.last_name,
            username=msg.from_user.username,
        )

    user.msg_count = user.msg_count + 1
    user.save()

    admins = get_admins() + [app.get_me().id]
    if msg.from_user.id in admins:
        return False

    patterns20 = cache.get('blacklist20', [])
    patterns = cache.get('blacklist', [])

    try:
        group = Group.objects.get(pk=msg.chat.id)
    except Group.DoesNotExist:
        msg = f'Group {msg.chat.title}({msg.chat.id}) is not a vendor'
        log(client, msg)
        return False

    if not group.antispam:
        return False

    text_hack = f" {msg.text.strip()} "
    if user.msg_count <= 20:
        for pattern in patterns20:
            res = pattern.regex.search(text_hack)
            if res is not None:
                msg.delete()
                """
                Send log to log group
                """
                if msg.chat.type == ChatType.SUPERGROUP or msg.chat.type == ChatType.GROUP:
                    logmsg = (
                        f'Message from {msg.from_user.mention} in '
                        f'{msg.chat.title} was deleted for blacklisted word'
                        f'/phrase\n<code>{msg.text}</code>\n'
                        f'Matched pattern: {pattern.regex}'
                    )
                    log(client, logmsg)
                    """
                    we can exit if we actually deleted a message
                    """
                return True

    """
    if there were no matches in the blacklist20
    then we proceed to the main blacklist
    """
    for pattern in patterns:
        res = pattern.regex.search(text_hack)
        if res is not None:
            msg.delete()
            """
            Send log to log group
            """
            if msg.chat.type == ChatType.SUPERGROUP or msg.chat.type == ChatType.GROUP:
                logmsg = (
                    f'Message from {msg.from_user.mention} in '
                    f'{msg.chat.title} was deleted for blacklisted word'
                    f'/phrase\n<code>{msg.text}</code>\n'
                    f'Matched pattern: {pattern.regex}'
                )
                log(client, logmsg)
            break


@app.on_message(filters.group, group=-1)
def handle_msg5(client, msg):
    if msg.text is None:
        return None

    group_id = msg.chat.id

    try:
        group_limits = Group.objects.get(group_id=group_id).group_limits
    except ObjectDoesNotExist:
        return None

    user_id = msg.from_user.id

    if user_id is None:
        return None

    if not is_admin(user_id):
        word_limit = group_limits.word_limit
        new_line_limit = group_limits.new_line_limit

        if word_limit is not None:
            if len(msg.text) > word_limit:
                msg.delete()
                return None

        if new_line_limit is not None:
            if msg.text.count('\n') > new_line_limit:
                msg.delete()
                return None

        sent = client.send_message(
            group_id,
            text=f'Hi {msg.mention}, Make sure your message doesnt contain more than {word_limit} words(including spaces) and {new_line_limit} lines.',
        )

        sched_cleanup(sent)

        return None


def initialize():
    print('Antispam module initialized')
    app.run()
