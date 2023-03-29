from django.db import models
from group.models import Group


class Captcha(models.Model):
    answer = models.IntegerField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE,
                              related_name='+')
    incorrect = models.IntegerField(default=0)

    class Meta:
        db_table = 'captchas'
