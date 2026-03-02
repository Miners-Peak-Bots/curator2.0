from .core import bot
from .sched import jobs
from user.models import TeleUser
from django.utils import timezone
from django.core.cache import cache
from blacklist.models import Blacklist


def load_blacklist_cache():
    """Load blacklist from DB into cache on startup"""
    # Load permanent blacklist
    blacklist = list(Blacklist.objects.filter(is_temp=False))
    cache.set('blacklist', blacklist)
    print(f"[Blacklist] Loaded {len(blacklist)} permanent entries into cache")
    
    # Load temp blacklist (first 20 messages)
    blacklist20 = list(Blacklist.objects.filter(is_temp=True))
    cache.set('blacklist20', blacklist20)
    print(f"[Blacklist] Loaded {len(blacklist20)} temp (20-msg) entries into cache")


def cron_job(bot, startup_check=None):
    for user in TeleUser.objects.filter(verified=True):
        expires_at = user.verification_expires_at

        expires_at_string = expires_at.strftime('%Y-%m-%d')

        if startup_check:
            is_notified = False
        else:
            is_notified = user.verification_expires_thirty_days_notification

        
        current_time = timezone.now()

        remaining_days = (expires_at - current_time).days

        if remaining_days < 0:
            user.verified = False
            user.verify_log(message=f"Verification expired on {current_time}", event=2)
            user.save()

            try:
                pyrogram_user_object = bot.get_users(user.tele_id)
                username_string = f'@{pyrogram_user_object.username}' if pyrogram_user_object.username else ''
                user_details = f"{pyrogram_user_object.mention} -- {username_string}"
                bot.send_message(user.tele_id, f"Your verification expired on {expires_at_string}")
            except Exception as exc:
                print(exc)
                first_name = user.first_name or ""
                last_name = user.last_name or ""
                full_name = f"{first_name} {last_name}"
                username_string = f'@{user.username}' if user.username else ''
                user_details = f"{full_name} -- {username_string}"

            message = f"Verification of {user_details} expired on {expires_at_string}"
            bot.send_message("@joe_sytneq", message)

        elif remaining_days <= 30 and is_notified is False:
            user.verification_expires_thirty_days_notification = True
            user.save()

            try:
                pyrogram_user_object = bot.get_users(user.tele_id)
                username_string = f'@{pyrogram_user_object.username}' if pyrogram_user_object.username else ''
                user_details = f"{pyrogram_user_object.mention} -- {username_string}"
                bot.send_message(
                    user.tele_id,
                    f"Your verification will expire at {expires_at_string} -- Remaining days: {remaining_days}",
                )
            except Exception as exc:
                first_name = user.first_name or ""
                last_name = user.last_name or ""
                full_name = f"{first_name} {last_name}"
                username_string = f'@{user.username}' if user.username else ''
                user_details = f"{full_name} -- {username_string}"

            message = (
                f"Verification of {user_details} will expire at {expires_at_string} -- Remaining days: {remaining_days}"
            )
            bot.send_message("@joe_sytneq", message)


def initialize():
    jobs.start()
    kwargs = {'bot': bot}

    # Load blacklist into cache before bot starts
    load_blacklist_cache()

    bot.start()
    from pyrogram import idle

    cron_job(bot, startup_check=True)
    jobs.add_job(cron_job, trigger='cron', day="*", hour=0, minute=0, second=0, kwargs=kwargs, id='cron-job')

    idle()

    bot.stop()
