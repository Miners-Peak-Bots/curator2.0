from .core import bot
from .sched import jobs
from user.models import TeleUser
from django.utils import timezone


def cron_job(bot):
    for user in TeleUser.objects.filter(verified=True):
        expires_at = user.verification_expires_at
        is_notified = user.verification_expires_thirty_days_notification
        current_time = timezone.now()

        remaining_days = (expires_at - current_time).days

        if remaining_days < 0:
            user.verified = False
            user.verify_log(message=f"Verification expired on {current_time}", event=2)
            user.save()

            try:
                pyrogram_user_object = bot.get_users(user.tele_id)
                user_details = f"{pyrogram_user_object.mention} -- {pyrogram_user_object.username}"
                bot.send_message(f"Your verification is expires on {expires_at}")
            except Exception:
                first_name = user.first_name or ""
                last_name = user.last_name or ""
                full_name = f"{first_name} {last_name}"
                user_details = f"{full_name} -- {user.username}"

            message = f"Verification of {user_details} expired on {expires_at}"
            bot.send_message("@joe_cryptech", message)

        elif remaining_days <= 30 and is_notified is False:
            user.verification_expires_thirty_days_notification = True
            user.save()

            try:
                pyrogram_user_object = bot.get_users(user.tele_id)
                user_details = f"{pyrogram_user_object.mention} -- {pyrogram_user_object.username}"
                bot.send_message(f"Your verification expires on {expires_at} -- Remaining days: {remaining_days}")
            except Exception:
                first_name = user.first_name or ""
                last_name = user.last_name or ""
                full_name = f"{first_name} {last_name}"
                user_details = f"{full_name} -- {user.username}"

            message = f"Verification of {user_details} expired on {expires_at} -- Remaining days: {remaining_days}"
            bot.send_message("@joe_cryptech", message)


def initialize():
    jobs.start()
    bot.run()
    kwargs = {'bot': bot}
    jobs.add_job(cron_job, trigger='cron', day="*", hour='*', minute=20, second=0, kwargs=kwargs, id='cron-job')
