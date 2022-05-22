from django.db import models
from pyrogram.types import ChatPermissions


class Group(models.Model):
    group_id = models.CharField(max_length=30, primary_key=True)
    permission = models.ForeignKey('group.Permission',
                                   on_delete=models.SET_NULL,
                                   null=True)
    enabled = models.BooleanField(default=True)
    log_channel = models.IntegerField(null=True)
    title = models.CharField(null=True, max_length=30)
    username = models.CharField(null=True, max_length=30)
    link = models.CharField(null=True, max_length=30)

    def __str__(self):
        if self.title:
            return f'{self.title}({self.group_id})'
        else:
            return self.group_id

    class Meta:
        db_table = 'groups'


class SpecialGroup(models.Model):
    group_id = models.CharField(max_length=30, primary_key=True)
    privilege = models.ForeignKey('group.Privilege',
                                  on_delete=models.SET_NULL,
                                  null=True)
    title = models.CharField(null=True, max_length=30)
    username = models.CharField(null=True, max_length=30)
    link = models.CharField(null=True, max_length=30)

    def __str__(self):
        if self.title:
            return f'{self.title}({self.group_id})'
        else:
            return self.group_id


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
    can_post_messages = models.BooleanField(default=False)
    can_edit_messages = models.BooleanField(default=False)
    can_invite_users = models.BooleanField(default=False)
    can_pin_messages = models.BooleanField(default=True)
    is_anonymous = models.BooleanField(default=False)

    def __str__(self):
        return self.name
