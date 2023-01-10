import os
from logzero import logger
from pyrogram import Client
import importlib
from django.conf import settings


class Curator(Client):
    def __init__(self,
                 name: str,
                 handler_path: str):
        self.name = name
        self.handler_path = handler_path
        self.help = []
        self.admin_manual = []
        self.help = []
        super().__init__(
            name=f'{os.getcwd()}/{name}',
            api_id=settings.BOT_API_ID,
            api_hash=settings.BOT_API_HASH,
            bot_token=settings.BOT_API_TOKEN
        )
        self.__attach_handlers()

    def __attach_manual(self, module):
        try:
            self.help.append(module.__HELP__)
        except Exception as e:
            print(str(e))
            pass

    def __attach_admin_manual(self, module):
        try:
            self.admin_manual.append(module.__HELP__ADMIN__)
        except Exception as e:
            print(str(e))
            pass

    def __attach_handlers(self):
        dis_allowed = ['__init__.py', '__pycache__']
        module_path = self.handler_path
        search_path = os.path.join(settings.BASE_DIR, module_path)
        import_path = module_path.replace('/', '.')

        modules = os.listdir(search_path)
        modules = [module for module in modules if module not in dis_allowed]
        modules = [module for module in modules if module[-4:] != '.pyc']
        for module in modules:
            logger.info(f'Attaching handlers in {module}')
            module_path = import_path+module.replace('.py', '')
            module_ = importlib.import_module(module_path)

            self.__attach_manual(module_)
            self.__attach_admin_manual(module_)

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
