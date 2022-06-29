from pyrogram import Client, idle, filters
from django.conf import settings
from blacklist.models import Blacklist
from user.models import TeleUser


api_id = settings.BOT_API_ID
api_hash = settings.BOT_API_HASH
token = settings.ANTISPAM_BOT_TOKEN

app = Client('antispam.bot', api_id=api_id, api_hash=api_hash,
             bot_token=token)


def get_patterns():
    return Blacklist.objects.all()


def get_admins():
    admins_all = TeleUser.objects.filter(admin=True).values_list('tele_id')
    admins = [admin[0] for admin in admins_all] + [settings.BOT_MASTER]
    return admins


patterns = get_patterns()
admins = get_admins()


@app.on_message(filters.regex('.+[\u4E00-\uA000]'))
def handle_msg(client, msg):
    msg.delete()


@app.on_message(filters.regex('.+[\u0600-\u06ff]'))
def handle_msg2(client, msg):
    msg.delete()


@app.on_message(filters.regex(
    '(https?:\/\/)?(www[.])?(telegram|t)\.me\/([a-zA-Z0-9_-]*)\/?$'))
def handle_msg3(client, msg):
    print('tele link detected')
    msg.delete()


@app.on_message(filters.text)
def handle_msg4(client, msg):
    user = msg.from_user.id
    if user in admins:
        return False
    for pattern in patterns:
        res = pattern.regex.search(msg.text)
        if res is not None:
            msg.delete()
            break


def initialize():
    print('Antispam module initialized')
    app.run()
    idle()
