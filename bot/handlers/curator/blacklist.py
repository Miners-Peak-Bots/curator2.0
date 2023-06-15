import re
from pyrogram.handlers import MessageHandler
from django.conf import settings
from pyrogram import filters
from blacklist.models import Blacklist
from pyrogram.enums import ParseMode
from django.core.cache import cache

CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def add_blacklist(client, msg):
    if msg.from_user.id not in settings.BOT_MASTER:
        msg.delete()
        return False

    if len(msg.command) == 1:
        msg.delete()
        return False

    if msg.command[1] == '~':
        phrase = msg.text.replace('$blacklist', '')
        phrase = ogphrase = phrase.replace('~', '').strip()
        if not len(phrase) >= 1:
            msg.delete()
            return False
    else:
        phrase = ogphrase = msg.text.replace('$blacklist', '').strip()
        if not len(phrase) >= 1:
            msg.delete()
            return False

        phrase = fr'\s+{re.escape(phrase)}\s+'

    query = Blacklist.objects.filter(regex=phrase, is_temp=False)
    if not query.count():
        try:
            word = Blacklist.objects.create(regex=phrase, is_temp=False)
        except Exception as e:
            msg.reply_text(str(e), parse_mode=ParseMode.HTML)
            return None

        blacklist = cache.get('blacklist', [])
        blacklist.append(word)
        cache.set('blacklist', blacklist)

    msg.reply_text(f'<code>{ogphrase.strip()}</code> has been added to blacklist.', parse_mode=ParseMode.HTML)


def whitelist(client, msg):
    if msg.from_user.id not in settings.BOT_MASTER:
        msg.delete()
        return False

    if len(msg.command) == 1:
        msg.delete()
        return False

    if msg.command[1] == '~':
        phrase = msg.text.replace('$whitelist', '')
        phrase = ogphrase = phrase.replace('~', '').strip()
        if not len(phrase) >= 1:
            msg.delete()
            return False
    else:
        phrase = ogphrase = msg.text.replace('$whitelist', '').strip()
        if not len(phrase) >= 1:
            msg.delete()
            return False
        phrase = fr'\s+{re.escape(phrase)}\s+'

    query = Blacklist.objects.filter(regex=phrase)
    if not query.count():
        msg.reply_text(f'<code>{ogphrase.strip()}</code> does not exist in blacklist', parse_mode=ParseMode.HTML)
        return False

    query.all().delete()
    blacklist = [row for row in Blacklist.objects.all()]
    cache.set('blacklist', blacklist)
    msg.reply_text(f'<code>{ogphrase.strip()}</code> has been whitelisted', parse_mode=ParseMode.HTML)


__HANDLERS__ = [
    MessageHandler(add_blacklist, filters.command('blacklist', prefixes=CMD_PREFIX)),
    MessageHandler(whitelist, filters.command('whitelist', prefixes=CMD_PREFIX)),
]


__HELP__ADMIN__ = (
    '$blacklist: Add a word/phrase to blacklist(Not case sensitive)\n'
    '    $blacklist Foobar\n'
    '$whitelist: Remove a word/phrase from blacklist'
    '    $whitelist Foobar\n'
)
