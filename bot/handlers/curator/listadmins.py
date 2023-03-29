from pyrogram.handlers import MessageHandler
from pyrogram.enums import ParseMode
from pyrogram import filters
from user.models import TeleUser
from django.conf import settings

CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def handle_lsadmins(client, msg):
    verified_l = TeleUser.objects.filter(admin=True)
    message = []
    for user in verified_l:
        message.append(
            f'{user.mention} | {user.first_name}'
        )
        # message.append(user.mention)
    users = '\n'.join(message)
    response = (
        f'⚜️<b>Administrators</b> ⚜️ \n\n'
        '<code>User | Name</code>\n\n'
        f'{users}\n\n'
    )
    msg.reply_text(response, parse_mode=ParseMode.HTML)
    pass


__HANDLERS__ = [
    MessageHandler(handle_lsadmins,
                   (
                       filters.command('listadmins', prefixes=CMD_PREFIX)
                       &
                       filters.private
                   )),
]


__HELP__ADMIN__ = (
    "$listadmins: Retrieve list of administrators"
)
