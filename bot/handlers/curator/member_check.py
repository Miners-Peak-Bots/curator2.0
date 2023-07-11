import time

from pyrogram import Client
from user.models import TeleUser
from group.models import Group

@Client.on_chat_member_updated(group=-1)
def member_check(client, msg):
    if not msg.old_chat_member and msg.new_chat_member:
        user_id = msg.new_chat_member.user.id
        try:
            user = TeleUser.objects.get(pk=user_id)
        except TeleUser.DoesNotExist:
            pass
        else:
            if user.verified:
                try:
                    group = Group.objects.get(pk=msg.chat.id, vendor=True)
                    privileges = group.get_special_privileges()
                    client.promote_chat_member(chat_id=group.group_id, user_id=user.tele_id, privileges=privileges)
                    time.sleep(2)
                    if group.flair:
                        print("Setting flair to ", group.flair)
                        client.set_administrator_title(group.group_id, user.tele_id, group.flair)
                except Group.DoesNotExist:
                    pass


__HANDLERS__ = []
