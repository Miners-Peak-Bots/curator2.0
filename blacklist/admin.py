from django.contrib import admin
from .models import Blacklist


class BlacklistAdmin(admin.ModelAdmin):
    pass


admin.site.register(Blacklist, BlacklistAdmin)
