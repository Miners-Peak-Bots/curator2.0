from bot import initialize
from django.core.cache import cache
from blacklist.models import Blacklist
from group.models import Group


def run(*args):
    """
    Load the blacklist cache
    """
    blacklist = [row for row in Blacklist.objects.filter(is_temp=False)]
    blacklist20 = [row for row in Blacklist.objects.filter(is_temp=True)]
    group_config = {}
    for group in Group.objects.all():
        group_config[group.group_id] = group.antispam

    cache.set('blacklist', blacklist)
    cache.set('blacklist20', blacklist20)
    cache.set('group_cfg', group_config)
    initialize()
