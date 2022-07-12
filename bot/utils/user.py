from user.models import TeleUser


def get_user_by_username(username):
    try:
        return TeleUser.objects.get(username=username)
    except TeleUser.DoesNotExist:
        raise


def get_user_by_id(userid):
    try:
        return TeleUser.objects.get(pk=userid)
    except TeleUser.DoesNotExist:
        raise


def get_target_user_and_reason(msg, ommit='!warn'):
    if msg.reply_to_message:
        reason = msg.text.replace(ommit, '').strip()
        if not len(reason) >= 1:
            raise Exception('Invalid reason')
        userid = msg.reply_to_message.from_user.id
        data = {'reason': reason}
        try:
            data['user'] = get_user_by_id(userid)
            return data
        except Exception:
            raise Exception('User not found')

    if len(msg.command) > 2:
        userid = msg.command[1]
        userid = userid.replace('@', '')
        reason = ' '.join(msg.command[2:])
        data = {'reason': reason}
        try:
            data['user'] = get_user_by_username(userid)
            return data
        except Exception:
            raise


def get_target_user(msg):
    if msg.reply_to_message:
        userid = msg.reply_to_message.from_user.id
        try:
            user = get_user_by_id(userid)
            return user
        except Exception:
            raise

    if len(msg.command) >= 1:
        userid = msg.command[1]
        userid = userid.replace('@', '')
        try:
            user = get_user_by_username(userid)
            return user
        except Exception:
            raise
    else:
        raise Exception('User not found')
