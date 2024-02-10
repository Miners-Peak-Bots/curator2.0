from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import emoji


class User(AbstractUser):
    pass


class Warn(models.Model):
    user = models.ForeignKey('user.TeleUser', on_delete=models.CASCADE, related_name='warning')
    admin = models.ForeignKey('user.TeleUser', on_delete=models.SET_NULL, null=True, related_name='dispatched_warn')
    reason = models.CharField(max_length=128)
    """
    Warn type can have two values
    0 - normal warn
    1 - banning warn
    """
    banning_warn = models.BooleanField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class TeleUserLog(models.Model):
    events = {
        0: 'warned',
        1: 'unwarned',
        2: 'banned',
        3: 'unbanned',
        4: 'muted',
        5: 'unmuted',
    }
    user = models.ForeignKey('user.TeleUser', on_delete=models.CASCADE, related_name='logs')
    reason = models.CharField(max_length=256, null=True)
    """
    0 - Warn
    1 - Unwarn
    2 - Ban
    3 - Unban
    4 - Mute
    5 - Unmute
    6 - Verified
    7 - Unverified
    """
    event = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def message(self):
        event_msg = self.events.get(self.event)
        return f'{self.created_at.date()} - {event_msg} - {self.reason}'


class TeleUserVerifyLog(models.Model):
    events = {1: 'Verified', 2: 'Unverified', 3: 'Renewed'}
    user = models.ForeignKey('user.TeleUser', on_delete=models.CASCADE, related_name='vlogs')
    event = models.IntegerField()
    reason = models.CharField(max_length=256, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def message(self):
        event_msg = self.events.get(self.event)
        return f'{event_msg}: {self.created_at.date()}'


class TeleUser(models.Model):
    tele_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=32, null=True, default=None, blank=True)
    first_name = models.CharField(max_length=64, null=True, default=None, blank=True)
    last_name = models.CharField(max_length=64, null=True, default=None, blank=True)
    captcha_solved = models.BooleanField(default=False, editable=False)
    verified = models.BooleanField(default=False, blank=True)
    verification_expires_at = models.DateTimeField(null=True)
    verification_expires_thirty_days_notification = models.BooleanField(default=False, null=True)
    email = models.CharField(max_length=40, null=True, blank=True)
    keybase = models.CharField(max_length=120, null=True, blank=True)
    ph_number = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    active = models.BooleanField(default=False, blank=True)  # set to True after user unmutes self
    muted = models.BooleanField(default=False, blank=True)  # muted status from warnings
    muted_until = models.DateTimeField(null=True)
    banned = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    helper_admin = models.BooleanField(default=False)
    msg_count = models.IntegerField(default=0)

    @property
    def keybase_link(self):
        if not self.keybase:
            return None
        return 'https://keybase.io/' + self.keybase

    @property
    def username_tag(self):
        if not self.username:
            return None
        return '@' + self.username

    @property
    def country_emoji(self):
        cntry = f':{self.country.title()}:'
        return emoji.emojize(cntry)

    @property
    def is_admin(self):
        if self.tele_id in settings.BOT_MASTER:
            return True
        if self.admin:
            return True
        return False

    def warn(self, admin, reason, banning_warn=False):
        return Warn.objects.create(user=self, reason=reason, admin=admin, banning_warn=banning_warn)

    def log(self, event, message=None):
        return TeleUserLog.objects.create(user=self, reason=message, event=event)

    def verify_log(self, event, message=None):
        return TeleUserVerifyLog.objects.create(user=self, reason=message, event=event)

    @property
    def mention(self):
        if not self.username:
            return f"<a href='tg://user?id={self.tele_id}'>{self.tele_id}</a>"
        else:
            return f"@{self.username}"

    class Meta:
        db_table = 'telegram_users'
