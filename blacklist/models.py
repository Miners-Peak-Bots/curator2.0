from django.db import models
from regex_field.fields import RegexField
import re


class Blacklist(models.Model):
    regex = RegexField(max_length=128, re_flags=re.IGNORECASE)

    def __str__(self):
        return str(self.regex)

    class Meta:
        db_table = 'blacklist'
