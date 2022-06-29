from pyrogram.handlers import MessageHandler
from django.conf import settings
from pyrogram import filters
from blacklist.models import Blacklist
from pyrogram.enums import ParseMode


__HELP__ = """Hey man
How is it going"""


def add_blacklist(client, msg):
    if msg.from_user.id != settings.BOT_MASTER:
        msg.delete()
        return False

    phrase = msg.text.replace('!blacklist', '').strip()
    if not len(phrase) >= 1:
        msg.delete()
        return False

    query = Blacklist.objects.filter(regex=phrase)
    if not query.count():
        Blacklist.objects.create(regex=phrase)
    msg.reply_text(
        f'<code>{phrase.strip()}</code> has been added to blacklist.',
        parse_mode=ParseMode.HTML
    )


def whitelist(client, msg):
    if msg.from_user.id != settings.BOT_MASTER:
        msg.delete()
        return False

    phrase = msg.text.replace('!whitelist', '').strip()
    if not len(phrase) >= 1:
        msg.delete()
        return False

    query = Blacklist.objects.filter(regex=phrase)
    if not query.count():
        msg.reply_text(
            f'<code>{phrase.strip()}</code> does not exist in blacklist',
            parse_mode=ParseMode.HTML
        )
        return False

    query.all().delete()
    msg.reply_text(
        f'<code>{phrase.strip()}</code> has been whitelisted',
        parse_mode=ParseMode.HTML
    )


__HANDLERS__ = [
    MessageHandler(add_blacklist, filters.command('blacklist',
                                                  prefixes='!')),
    MessageHandler(whitelist, filters.command('whitelist',
                                              prefixes='!')),
]
