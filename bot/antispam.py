from pyrogram import Client, idle, filters
from django.conf import settings
from user.models import TeleUser
from bot.utils.msg import log
from pyrogram.enums import ChatType
from django.core.cache import cache

api_id = settings.BOT_API_ID
api_hash = settings.BOT_API_HASH
token = settings.ANTISPAM_BOT_TOKEN

app = Client('antispam.bot', api_id=api_id, api_hash=api_hash, bot_token=token)

msgcount = {}

def get_admins():
    admins_all = TeleUser.objects.filter(admin=True).values_list('tele_id')
    admins = [admin[0] for admin in admins_all] + [settings.BOT_MASTER]
    return admins


@app.on_message(filters.regex('.+[\u4E00-\uA000]'))
def handle_msg(client, msg):
    msg.delete()


@app.on_message(filters.regex('.+[\u0600-\u06ff]'))
def handle_msg2(client, msg):
    msg.delete()


@app.on_message(filters.regex('(https?:\/\/)?(www[.])?(telegram|t)\.me\/([a-zA-Z0-9_-]*)\/?$'))
def handle_msg3(client, msg):
    print('tele link detected')
    msg.delete()


@app.on_message(filters.text)
def handle_msg4(client, msg):
    try:
        current_count = msgcount[msg.from_user.id]
    except KeyError:
        current_count = 0

    current_count = current_count + 1
    msgcount[msg.from_user.id] = current_count

    print(msgcount)
    admins = get_admins()
    if msg.from_user.id in admins:
        return False

    if current_count <= 20:
        print('user has less than 20 scanning')

    patterns20 = cache.get('blacklist20', [])
    patterns = cache.get('blacklist', [])
    for pattern in patterns:
        res = pattern.regex.search(msg.text)
        if res is not None:
            msg.delete()
            """
            Send log to log group
            """
            if msg.chat.type == ChatType.SUPERGROUP or msg.chat.type == ChatType.GROUP:
                print('group detected')
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
