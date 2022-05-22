from ...db.cache import users_cache, groups_cache
from ...db.models import Group, User
from pyrogram.handlers import MessageHandler
from ...utils.user import get_user, create_user
import peewee
import emoji
from pyrogram import filters


__HELP__ = """Hey man
How is it going"""


def prep_message(user):
    text = f'User id: {user.user_id}\n'
    if user.first_name:
        text = text + f'First name: {user.first_name}\n'
    if user.username:
        text = text + f'Username: @{user.username}\n'
    if user.country:
        country = emoji.emojize(f':{user.country}:'.title())
        text = text + f'Country: {country}\n'
    if user.verified:
        text = text + emoji.emojize(':check_mark_button: Verified')

    return text


async def handle_check(client, msg):
    if not msg.reply_to_message:
        await msg.delete()
        return False

    member = msg.reply_to_message.from_user
    user_id = member.id
    try:
        user = get_user(user_id)
    except peewee.DoesNotExist:
        # await msg.reply_text('User not found in database')
        """
        Create the user
        """
        user = create_user(member)

    response = prep_message(user)
    await msg.reply_text(response)


__HANDLERS__ = [
    MessageHandler(handle_check, filters.command('check', prefixes='!'))
]
