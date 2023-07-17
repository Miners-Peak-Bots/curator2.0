from .core import bot
from .sched import jobs


def initialize():
    jobs.start()
    bot.run()
