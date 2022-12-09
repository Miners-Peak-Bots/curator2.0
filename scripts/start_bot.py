from bot import initialize
from django.core.cache import cache
from blacklist.models import Blacklist


def run(*args):
    """
    Load the blacklist cache
    """
    blacklist = [row for row in Blacklist.objects.filter(is_temp=False)]
    blacklist20 = [row for row in Blacklist.objects.filter(is_temp=True)]
    cache.set('blacklist', blacklist)
    cache.set('blacklist20', blacklist20)
    initialize()
