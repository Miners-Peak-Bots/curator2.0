from django.contrib import admin
from .models import TeleUser


class TeleUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(TeleUser, TeleUserAdmin)
