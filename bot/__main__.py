import asyncio
from .core import bot
from pyrogram import idle


async def initialize():
    await bot.start()
    await idle()


if __name__ == '__main__':
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loopu)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(initialize())
