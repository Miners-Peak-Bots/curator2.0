from django.contrib import admin
from .models import (
    Group,
    # SpecialGroup,
    Permission,
    Privilege
)


class GroupAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'vendor', 'title']
    list_filter = ['vendor']
    search_fields = ['title', 'group_id']
    search_help_text = "Search by name or group id"
    readonly_fields = ('group_id', 'title', 'username', 'link')


# class SpecialGroupAdmin(admin.ModelAdmin):
#     pass


class PermissionAdmin(admin.ModelAdmin):
    pass


class PrivilegeAdmin(admin.ModelAdmin):
    readonly_fields = ['is_anonymous']


admin.site.register(Group, GroupAdmin)
# admin.site.register(Group, SpecialGroupAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Privilege, PrivilegeAdmin)
