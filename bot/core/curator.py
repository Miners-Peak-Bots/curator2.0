import os
import pathlib
from logzero import logger
from typing import Union
from ..core import config_engine
from pyrogram import Client
import importlib
from django.conf import settings


class Curator(Client):
    def __init__(self,
                 name: str,
                 config: Union[str, pathlib.Path, dict]):
        self.name = name
        self.help = []
        super().__init__(
            name=f'{os.getcwd()}/{name}',
            api_id=settings.BOT_API_ID,
            api_hash=settings.BOT_API_HASH,
            bot_token=settings.BOT_API_TOKEN
        )
        self.__attach_handlers()

    def __attach_handlers(self):
        dis_allowed = ['__init__.py', '__pycache__']
        module_path = 'bot/handlers/bot_handlers/'
        search_path = os.path.join(settings.BASE_DIR, module_path)
        import_path = module_path.replace('/', '.')

        modules = os.listdir(search_path)
        modules = [module for module in modules if module not in dis_allowed]
        modules = [module for module in modules if module[-4:] != '.pyc']
        for module in modules:
            logger.info(f'Attaching handlers in {module}')
            module_path = import_path+module.replace('.py', '')
            module_ = importlib.import_module(module_path)
            self.help.append(module_.__HELP__)
            for handler in module_.__HANDLERS__:
                if isinstance(handler, list):
                    event_handler = handler[0],
                    group = handler[1]
                    self.add_handler(event_handler, group=group)
                else:
                    self.add_handler(handler)

    def start(self):
        super().start()
        self.me = self.get_me()
        logger.info(f'{self.name} started')

    def stop(self):
        logger.info(f'{self.name} stopped')
