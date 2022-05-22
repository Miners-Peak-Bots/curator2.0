from django.contrib import admin
from .models import (
    Group,
    SpecialGroup,
    Permission,
    Privilege
)


class GroupAdmin(admin.ModelAdmin):
    pass


class SpecialGroupAdmin(admin.ModelAdmin):
    pass


class PermissionAdmin(admin.ModelAdmin):
    pass


class PrivilegeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Group, GroupAdmin)
admin.site.register(SpecialGroup, SpecialGroupAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Privilege, PrivilegeAdmin)
