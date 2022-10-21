from django.contrib import admin
from .models import TeleUser


class TeleUserAdmin(admin.ModelAdmin):
    # readonly_fields = ("captcha_solved", "verified", "muted_until")
    readonly_fields = ('tele_id', 'username', 'first_name', 'last_name',
                       'verified', 'admin', 'banned', 'muted_until', 'muted',
                       'active',)
    pass


admin.site.register(TeleUser, TeleUserAdmin)
