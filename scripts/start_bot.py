from bot import initialize
from django.core.cache import cache
from blacklist.models import Blacklist


def run(*args):
    """
    Load the blacklist cache
    """
    query = Blacklist.objects.all()
    blacklist = [row for row in query]
    cache.set('blacklist', blacklist)
    initialize()
