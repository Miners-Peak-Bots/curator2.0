from django.db import models
from pyrogram.types import (
    ChatPermissions,
    ChatPrivileges
)


class Group(models.Model):
    group_id = models.CharField(max_length=30, primary_key=True)
    permission = models.ForeignKey('group.Permission',
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True)
    verified_privilege = models.ForeignKey('group.Privilege',
                                           help_text=(
                                               'Privileges for verified'
                                               'users'
                                           ),
                                           on_delete=models.SET_NULL,
                                           null=True,
                                           blank=True)
    admin_privilege = models.ForeignKey('group.Privilege',
                                        help_text=(
                                            'Privileges for admins'
                                        ),
                                        on_delete=models.SET_NULL,
                                        null=True,
                                        related_name='+',
                                        blank=True)
    shortname = models.CharField(max_length=30, null=True, blank=True,
                                 unique=True)
    special = models.BooleanField(default=False)
    enabled = models.BooleanField(default=True)
    log_channel = models.IntegerField(null=True, blank=True)
    title = models.CharField(null=True, max_length=30, blank=True)
    username = models.CharField(null=True, max_length=30, blank=True)
    link = models.CharField(null=True, max_length=30, blank=True)

    def __str__(self):
        if self.title:
            return f'{self.title}({self.group_id})'
        else:
            return self.group_id

    def get_admin_privileges(self):
        if self.admin_privilege:
            return self.admin_privilege.get_privileges()
        else:
            return ChatPrivileges(can_change_info=True)

    def get_permissions(self):
        if self.permission:
            return self.permission.get_permissions()
        else:
            return ChatPermissions(can_send_messages=True)

    def get_special_privileges(self):
        if self.verified_privilege:
            return self.verified_privilege.get_privileges()
        else:
            return ChatPrivileges(can_change_info=True)

    class Meta:
        db_table = 'groups'


class Permission(models.Model):
    name = models.CharField(max_length=20)
    can_send_messages = models.BooleanField(default=True)
    can_send_media_messages = models.BooleanField(default=False)
    can_send_other_messages = models.BooleanField(default=False)
    can_send_polls = models.BooleanField(default=False)
    can_add_web_page_previews = models.BooleanField(default=False)
    can_change_info = models.BooleanField(default=False)
    can_invite_users = models.BooleanField(default=False)
    can_pin_messages = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Privilege(models.Model):
    name = models.CharField(max_length=20)
    can_manage_chat = models.BooleanField(default=False)
    can_delete_messages = models.BooleanField(default=False)
    can_manage_video_chats = models.BooleanField(default=False)
    can_restrict_members = models.BooleanField(default=False)
    can_promote_members = models.BooleanField(default=False)
    can_change_info = models.BooleanField(default=False)
    can_post_messages = models.BooleanField(default=False,
                                            help_text="Only for channels")
    can_edit_messages = models.BooleanField(default=False,
                                            help_text="Only for channels")
    can_invite_users = models.BooleanField(default=False)
    can_pin_messages = models.BooleanField(default=True)
    is_anonymous = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_privileges(self):
        return ChatPrivileges(
            can_manage_chat=self.can_manage_chat,
            can_delete_messages=self.can_delete_messages,
            can_manage_video_chats=self.can_manage_video_chats,
            can_restrict_members=self.can_restrict_members,
            can_promote_members=self.can_promote_members,
            can_change_info=self.can_change_info,
            can_post_messages=self.can_post_messages,
            can_edit_messages=self.can_edit_messages,
            can_invite_users=self.can_invite_users,
            can_pin_messages=self.can_pin_messages,
            is_anonymous=self.is_anonymous
        )
