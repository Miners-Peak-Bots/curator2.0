from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    pass


class Warn(models.Model):
    user = models.ForeignKey('user.TeleUser',
                             on_delete=models.CASCADE,
                             related_name='warning')
    admin = models.ForeignKey('user.TeleUser',
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='dispatched_warn')
    reason = models.CharField(max_length=128)
    """
    Warn type can have two values
    0 - normal warn
    1 - banning warn
    """
    banning_warn = models.BooleanField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class TeleUser(models.Model):
    tele_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=32, null=True, default=None)
    first_name = models.CharField(max_length=64, null=True, default=None)
    last_name = models.CharField(max_length=64, null=True, default=None)
    captcha_solved = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    email = models.CharField(max_length=40, null=True)
    keybase = models.CharField(max_length=120, null=True)
    ph_number = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=20, null=True)
    active = models.BooleanField(default=False)  # set to True after user unmutes self
    muted = models.BooleanField(default=False)  # muted status from warnings
    muted_until = models.DateTimeField(null=True)
    banned = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def keybase_link(self):
        if not self.keybase:
            return None
        return 'https://keybase.io/'+self.keybase

    @property
    def username_tag(self):
        if not self.username:
            return None
        return '@'+self.username

    @property
    def is_admin(self):
        if self.tele_id == settings.BOT_MASTER:
            return True
        if self.admin:
            return True
        return False

    def warn(self, admin, reason, banning_warn=False):
        return Warn.objects.create(
            user=self,
            reason=reason,
            admin=admin,
            banning_warn=banning_warn
        )

    class Meta:
        db_table = 'telegram_users'


class TeleUserLog(models.Model):
    user = models.ForeignKey(TeleUser,
                             on_delete=models.CASCADE,
                             related_name='logs')
    reason = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
