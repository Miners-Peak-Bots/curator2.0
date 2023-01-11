from pyrogram import Client, idle, filters
from django.conf import settings
from user.models import TeleUser
from bot.utils.msg import log
from pyrogram.enums import ChatType
from django.core.cache import cache
from group.models import Group


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


@app.on_message(filters.regex('.+[\u4E00-\uA000]'))
def handle_msg(client, msg):
    msg.delete()


@app.on_message(filters.regex('.+[\u0600-\u06ff]'))
def handle_msg2(client, msg):
    msg.delete()


@app.on_message(filters.regex('(https?:\/\/)?(www[.])?(telegram|t)\.me\/([a-zA-Z0-9_-]*)\/?$'))
def handle_msg3(client, msg):
    msg.delete()


@app.on_message(filters.text)
def handle_msg4(client, msg):
    try:
        user = TeleUser.objects.get(pk=msg.from_user.id)
    except TeleUser.DoesNotExist:
        user = TeleUser.objects.create(tele_id=msg.from_user.id,
                                       first_name=msg.from_user.first_name,
                                       last_name=msg.from_user.last_name,
                                       username=msg.from_user.username)

    user.msg_count = user.msg_count + 1
    user.save()

    admins = get_admins()
    if msg.from_user.id in admins:
        return False

    patterns20 = cache.get('blacklist20', [])
    patterns = cache.get('blacklist', [])

    try:
        group = Group.objects.get(pk=msg.chat.id)
    except Group.DoesNotExist:
        msg = f'Group {msg.chat.title}({msg.chat.id}) not found in db'
        log(client, msg)
        return False

    if not group.antispam:
        return False

    if user.msg_count <= 20:
        for pattern in patterns20:
            res = pattern.regex.search(msg.text)
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
        res = pattern.regex.search(msg.text)
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


def initialize():
    print('Antispam module initialized')
    app.start()
    idle()
