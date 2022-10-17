from django.contrib import admin
from .models import TeleUser


class TeleUserAdmin(admin.ModelAdmin):
    # readonly_fields = ("captcha_solved", "verified", "muted_until")
    pass


admin.site.register(TeleUser, TeleUserAdmin)
