from pyrogram import Client, idle, filters
from django.conf import settings
from blacklist.models import Blacklist
from user.models import TeleUser
from bot.utils.msg import log
from pyrogram.enums import ChatType
from django.core.cache import cache

api_id = settings.BOT_API_ID
api_hash = settings.BOT_API_HASH
token = settings.ANTISPAM_BOT_TOKEN

app = Client('antispam.bot', api_id=api_id, api_hash=api_hash, bot_token=token)


def get_patterns():
    return Blacklist.objects.all()


def get_admins():
    admins_all = TeleUser.objects.filter(admin=True).values_list('tele_id')
    admins = [admin[0] for admin in admins_all] + [settings.BOT_MASTER]
    return admins


data = {
    'patterns': get_patterns(),
    'admins': get_admins(),
}


@app.on_message(filters.regex('.+[\u4E00-\uA000]'))
def handle_msg(client, msg):
    msg.delete()


@app.on_message(filters.regex('.+[\u0600-\u06ff]'))
def handle_msg2(client, msg):
    msg.delete()


@app.on_message(filters.command('refreshbl'))
def handle_refresh_bl(client, msg):
    data['patterns'] = get_patterns()
    msg.reply_text('Blacklist updated')


@app.on_message(filters.command('refreshadmins'))
def handle_refresh_admin(client, msg):
    data['admins'] = get_admins()
    msg.reply_text('Admins list updated')


@app.on_message(filters.regex('(https?:\/\/)?(www[.])?(telegram|t)\.me\/([a-zA-Z0-9_-]*)\/?$'))
def handle_msg3(client, msg):
    print('tele link detected')
    msg.delete()


@app.on_message(filters.text)
def handle_msg4(client, msg):
    # user = msg.from_user.id
    # if user in data['admins']:
    #     return False
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
