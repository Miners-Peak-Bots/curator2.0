from blacklist.models import Blacklist
from logzero import logger


def run(**args):
    with open('regex_blacklist.txt') as f:
        lines = f.readlines()
        patterns = []
        for line in lines:
            phrase = line.strip()
            patterns.append(Blacklist(regex=phrase))

        Blacklist.objects.bulk_create(patterns)
        logger.info(f'Added {len(patterns)} regex patterns')
