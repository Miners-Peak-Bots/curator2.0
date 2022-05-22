from pydantic import BaseModel
from typing import List, Optional


class TModel(BaseModel):
    class Config:
        orm_mode = True


class Settings(TModel):
    group_id: int
    join_greeting_enabled: bool
    exit_greeting_enabled: bool
    service_removal_enabled: bool
    raid_mode_enabled: bool


class Group(TModel):
    group_id: int
    enabled: bool


class Warns(TModel):
    user_id: int
    group_id: int
    reason: str
    log_group: int
    log_message_id: int


class User(TModel):
    user_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    # warns: Optional[List[Warns]]
