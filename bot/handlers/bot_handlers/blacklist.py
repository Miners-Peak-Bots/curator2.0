from ...db.cache import users_cache, groups_cache
from ...db.models import Blacklist
from pyrogram.handlers import MessageHandler
import peewee
from pyrogram import filters


__HELP__ = """Hey man
How is it going"""


async def handle_add_blacklist_words(client, msg):
    if msg.from_user.id != client.config.general.master_id:
        return False

    words = msg.command[1:]
    words = [word.lower() for word in words]
    for word in words:
        bl, created = Blacklist.get_or_create(phrase=word)
        bl.save()

    await msg.reply_text(
        ', '.join(words) + ' have been added to blacklist'
    )


async def handle_add_blacklist_phrase(client, msg):
    if msg.from_user.id != client.config.general.master_id:
        return False

    command = '/blacklistp'
    phrase = msg.text.replace(command, '').strip().lower()
    bl, created = Blacklist.get_or_create(phrase=phrase)

    await msg.reply_text(
        f"```{phrase}```\nhas been added to blacklist"
    )


async def handle_whitelist(client, msg):
    command = '/whitelist'
    phrase = msg.text.replace(command, '').strip().lower()
    try:
        row = Blacklist.get(Blacklist.phrase == phrase)
        row.enabled = False
        row.save()

        await msg.reply_text(
            phrase + ' has been whitelisted'
        )
    except peewee.DoesNotExist:
        await msg.reply_text(
            phrase + ' does not exist in blacklist'
        )


async def view_blacklist(client, msg):
    if msg.from_user.id != client.config.general.master_id:
        return False

    phrases = []
    for row in Blacklist.select().where(Blacklist.enabled == 1):
        phrases.append(row.phrase)

    await msg.reply_text(
        '\n'.join(phrases)
    )


__HANDLERS__ = [
    MessageHandler(handle_whitelist, filters.command('whitelist',
                                                     prefixes='!')),
    MessageHandler(handle_add_blacklist_words, filters.command('blacklistw',
                                                               prefixes='!')),
    MessageHandler(handle_add_blacklist_phrase, filters.command('blacklistp',
                                                                prefixes='!')),
    MessageHandler(view_blacklist, filters.command('blist', prefixes='!')),
]
