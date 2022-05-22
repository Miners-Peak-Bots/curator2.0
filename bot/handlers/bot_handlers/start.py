from ...db.cache import users_cache, groups_cache, misc
from pyrogram.handlers import MessageHandler
from ...utils.user import get_user
from pyrogram import filters
import peewee

__HELP__ = """Hey man
How is it going"""


async def handle_review(client, msg):
    try:
        user_id = int(msg.command[1])
    except ValueError:
        await msg.reply_text('Invalid action')
        return False

    try:
        user = get_user(user_id)
    except peewee.DoesNotExist:
        await msg.reply_text('User not found')
        return False

    stars_service = await client.ask(msg.chat.id,
                                     'How many stars out of 5?')
    stars_service = stars_service.text
    print(stars_service)


async def handle_start(client, msg):
    if len(msg.command) > 1:
        """
        This is a deep linked message for reviewing sellers.
        Pass to another method
        """
        await handle_review(client, msg)
        return False

    await msg.reply_text('I am a private group administration robot.')

__HANDLERS__ = [
    MessageHandler(handle_start, filters.command('start', '/'))
]
