from blacklist.models import Blacklist
from logzero import logger


def run(**args):
    with open('patterns.txt') as f:
        patterns = f.readlines()

    patterns = [
        Blacklist(regex=pattern.strip())
        for
        pattern in patterns
    ]
    inserted = Blacklist.objects.bulk_create(patterns)
    logger.info(f'Inserted {len(inserted)} patterns')
