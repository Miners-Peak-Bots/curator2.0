from django.conf import settings
from logzero import logger
from pyrogram.enums import ParseMode


def errorify(msg, erray):
    errors = f'Errors occured: {len(erray)}\n'
    errors = errors + '<code>' + '\n'.join(erray) + '</code>'
    return msg + '\n\n' + errors


def titlefy(key, value, nl=False):
    if not nl:
        return f'<b>{key}:</b> <code>{value}</code>\n'
    else:
        return f'<b>{key}:</b>\n<code>{value}</code>\n'


def linkify(url, text, bold=False):
    text = f"<a href='{url}'>{text}</a>"
    if bold:
        return f'<b>{text}</b>'
    else:
        return text


def titlefy_simple(key, value, nl=False):
    if not nl:
        return f'<b>{key}:</b> {value}\n'
    else:
        return f'<b>{key}:</b>\n{value}\n'


def boldify(phrase):
    return f'<b>{phrase}</b>'


def log(client, message):
    try:
        client.send_message(
            chat_id=settings.LOG_GROUP,
            text=message,
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        logger.error(e)
