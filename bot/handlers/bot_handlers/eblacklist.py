from ...db.cache import users_cache, groups_cache
from ...db.models import EntityBlacklist
from ...utils.group import parse_entities
from pyrogram.handlers import MessageHandler
import peewee
from pyrogram import filters


__HELP__ = """Hey man
How is it going"""


def handle_add_blacklist_words(client, msg):
    if msg.from_user.id != client.config.general.master_id:
        return False

    words = msg.command[1:]
    words = [word.lower() for word in words]
    for word in words:
        bl, created = EntityBlacklist.get_or_create(token=word)
        bl.save()

    msg.reply_text(
        ', '.join(words) + ' have been added to blacklist'
    )


def handle_add_blacklist_token(client, msg):
    if msg.from_user.id != client.config.general.master_id:
        return False

    entities = parse_entities(msg)
    tokens = []
    token_phrases = []
    for entity in entities:
        append = EntityBlacklist(
            token_type=entity['token_type'],
            token=entity['token'],
        )
        tokens.append(append)
        token_phrases.append(entity['token'])

    EntityBlacklist.bulk_create(tokens)
    tokens = '<code>' + '\n'.join(token_phrases) + '</code>'

    msg.reply_text(tokens + '\nhave been added')


def handle_whitelist(client, msg):
    command = '/whitelist'
    token = msg.text.replace(command, '').strip().lower()
    try:
        row = EntityBlacklist.get(EntityBlacklist.token == token)
        row.enabled = False
        row.save()

        msg.reply_text(
            token + ' has been whitelisted'
        )
    except peewee.DoesNotExist:
        msg.reply_text(
            token + ' does not exist in blacklist'
        )


def view_blacklist(client, msg):
    if msg.from_user.id != client.config.general.master_id:
        return False

    tokens = []
    for row in EntityBlacklist.select().where(EntityBlacklist.enabled == 1):
        tokens.append(row.full_token)

    tokens = '<code>' + '\n'.join(tokens) + '</code>'
    msg.reply_text(tokens)


__HANDLERS__ = [
    MessageHandler(handle_whitelist, filters.command('ewhitelist',
                                                     prefixes='!')),
    MessageHandler(handle_add_blacklist_token, filters.command('eblacklist',
                                                               prefixes='!')),
    MessageHandler(view_blacklist, filters.command('eblist', prefixes='!')),
]
