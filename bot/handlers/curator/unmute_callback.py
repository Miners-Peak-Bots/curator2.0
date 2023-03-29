from pyrogram.handlers import CallbackQueryHandler
from pyrogram import filters
from captcha.models import Captcha
from captcha.lib import CaptchaEngine


def handle_unmute_callback(client, callback_query):
    _, captcha_id, answer = callback_query.data.split('_')
    user_id = callback_query.from_user.id

    try:
        captcha = Captcha.objects.get(pk=captcha_id)
    except Captcha.DoesNotExist:
        callback_query.answer('An unexpected error occured')
        return False

    try:
        captcha_id = int(captcha_id)
    except ValueError:
        # Malicious input?
        callback_query.answer('Invalid response type')
        return False

    try:
        answer = int(answer)
    except ValueError:
        # Malicious input?
        callback_query.answer('Invalid response type')
        return False

    if captcha.answer == answer:
        callback_query.answer(text="Congrats your request to join group has been accepted", show_alert=True)
        client.approve_chat_join_request(captcha.group_id, user_id)
        callback_query.message.edit_reply_markup(
            reply_markup=None,
        )
        return True
    else:
        incorrect = captcha.incorrect + 1
        if incorrect >= 3:
            callback_query.answer(
                text=(
                    'You failed to solve the captcha. '
                    'Contact an admin to join group.'
                ),
                show_alert=True)
            callback_query.message.delete()
            captcha.delete()
        else:
            new_captcha = CaptchaEngine()
            captcha.answer = new_captcha.ans
            captcha.incorrect = incorrect
            captcha.save()
            callback_query.message.edit_text(
                text=new_captcha.msg(),
                reply_markup=new_captcha.keyboard(captcha.id)
            )
            callback_query.answer('Wrong answer! Try again', show_alert=True)

        return False


__HANDLERS__ = [
    CallbackQueryHandler(handle_unmute_callback, filters.regex('umt_'))
]
