from pydantic import BaseModel
from typing import Optional, Union
from logzero import logger
import pathlib


class General(BaseModel):
    api_id: int
    api_hash: str
    bot_token: str
    phone_number: str
    master_id: int
    bot_username: Optional[str]


class Config(BaseModel):
    general: General


def load_config(config: Union[str, pathlib.Path, dict]) -> Config:
    if isinstance(config, dict):
        parse = Config.parse_obj
    elif isinstance(config, pathlib.Path):
        parse = Config.parse_file
    elif isinstance(config, str):
        """
            Check if its a valid path using pathlib, if not its json
        """
        p = pathlib.Path(config)
        if not p.exists() or not p.is_file():
            parse = Config.parse_raw
        else:
            parse = Config.parse_file
            config = p

    try:
        return parse(config)
    except Exception as e:
        logger.error('Error reading config file, exitting.')
        logger.error(str(e))
        logger.error('Exiting')
        quit()
