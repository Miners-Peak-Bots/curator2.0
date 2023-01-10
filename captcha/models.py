from django.db import models
from group.models import Group


class Captcha(models.Model):
    answer = models.IntegerField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE,
                              related_name='+')

    class Meta:
        db_table = 'captchas'
