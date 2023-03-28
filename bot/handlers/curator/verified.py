from pyrogram.handlers import MessageHandler
from pyrogram.enums import ParseMode
from pyrogram import filters
from user.models import TeleUser
from django.conf import settings

CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def handle_verified(client, msg):
    verified_l = TeleUser.objects.filter(verified=True)
    message = []
    for user in verified_l:
        message.append(
            f'{user.country_emoji} | {user.mention} | {user.first_name}'
        )
        # message.append(user.mention)
    users = '\n'.join(message)
    response = (
        f'⚜️<b>Verified Users</b> ⚜️ - Randomized 25\n\n'
        '<code>Country | User | Name</code>\n\n'
        f'{users}\n\n'
        '<b>Powered by</b> @HardwareMarket'
    )
    msg.reply_text(response, parse_mode=ParseMode.HTML)
    pass


__HANDLERS__ = [
    MessageHandler(handle_verified,
                   (
                       filters.command('verified', prefixes=CMD_PREFIX)
                       &
                       filters.private
                   )),
]


__HELP__ = (
    "$verified: Print a list of verified users"
)
