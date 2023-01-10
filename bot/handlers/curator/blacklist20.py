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

    phrase = msg.text.replace('$blacklist20', '').strip()
    if not len(phrase) >= 1:
        msg.delete()
        return False

    ogphrase = phrase
    phrase = f'\\b{phrase}\\b'
    query = Blacklist.objects.filter(regex=phrase)
    if not query.count():
        word = Blacklist.objects.create(regex=phrase, is_temp=True)
        blacklist = cache.get('blacklist20', [])
        blacklist.append(word)
        cache.set('blacklist20', blacklist)

    msg.reply_text(
        f'<code>{ogphrase.strip()}</code> has been added to blacklist.',
        parse_mode=ParseMode.HTML
    )


def whitelist(client, msg):
    if msg.from_user.id not in settings.BOT_MASTER:
        msg.delete()
        return False

    phrase = msg.text.replace('$whitelist20', '').strip()
    if not len(phrase) >= 1:
        msg.delete()
        return False

    ogphrase = phrase
    phrase = f'\\b{phrase}\\b'
    query = Blacklist.objects.filter(regex=phrase, is_temp=True)
    if not query.count():
        msg.reply_text(
            f'<code>{ogphrase.strip()}</code> does not exist in blacklist',
            parse_mode=ParseMode.HTML
        )
        return False

    query.all().delete()
    blacklist = [row for row in Blacklist.objects.filter(is_temp=True)]
    cache.set('blacklist20', blacklist)
    msg.reply_text(
        f'<code>{ogphrase.strip()}</code> has been whitelisted',
        parse_mode=ParseMode.HTML
    )


__HANDLERS__ = [
    MessageHandler(add_blacklist, filters.command('blacklist20',
                                                  prefixes=CMD_PREFIX)),
    MessageHandler(whitelist, filters.command('whitelist20',
                                              prefixes=CMD_PREFIX)),
]


__HELP__ADMIN__ = (
    '$blacklist20: Add a word/phrase to blacklist(Not case sensitive)\n'
    '    $blacklist Foobar\n'
    '$whitelist20: Remove a word/phrase from blacklist'
    '    $whitelist Foobar\n'
)
