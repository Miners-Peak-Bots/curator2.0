from peewee import (SqliteDatabase,
                    Model,
                    IntegerField,
                    ForeignKeyField,
                    BooleanField,
                    CharField,
                    TextField,
                    DateTimeField)
import datetime
from playhouse.hybrid import hybrid_property

db = SqliteDatabase('curator.db')


class Group(Model):
    group_id = IntegerField(primary_key=True)
    enabled = BooleanField(default=True)
    log_channel = IntegerField(null=True)
    title = CharField(null=True)
    username = CharField(null=True)
    link = CharField(null=True)

    class Meta:
        database = db
        db_table = 'groups'


class Settings(Model):
    group_id = ForeignKeyField(Group, field='group_id', backref='settings')
    join_greeting_enabled = BooleanField(default=False)
    exit_greeting_enabled = BooleanField(default=False)
    service_removal_enabled = BooleanField(default=False)
    raid_mode_enabled = BooleanField(default=False)

    class Meta:
        database = db
        db_table = 'settings'


class User(Model):
    user_id = IntegerField(primary_key=True)
    username = CharField(max_length=32, null=True, default=None)
    first_name = CharField(max_length=64, null=True, default=None)
    last_name = CharField(max_length=64, null=True, default=None)
    captcha_solved = BooleanField(default=False)
    verified = BooleanField(default=False)
    email = CharField(max_length=40, null=True)
    keybase = CharField(max_length=120, null=True)
    ph_number = CharField(max_length=20, null=True)
    country = CharField(max_length=20, null=True)
    active = BooleanField(default=False)  # set to True after user unmutes self
    muted = BooleanField(default=False)  # muted status from warnings
    muted_until = DateTimeField(null=True)
    banned = BooleanField(default=False)
    admin = BooleanField(default=False)

    class Meta:
        database = db
        db_table = 'users'

    @hybrid_property
    def keybase_link(self):
        if not self.keybase:
            return None
        return 'https://keybase.io/'+self.keybase

    @hybrid_property
    def username_tag(self):
        if not self.username:
            return None
        return '@'+self.username


class UserLog(Model):
    user = ForeignKeyField(User, field='user_id', backref='log')
    message = TextField()
    date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        db_table = 'userlog'


class Rep(Model):
    user = ForeignKeyField(User, field='user_id', backref='rep')
    created_by = ForeignKeyField(User, field='user_id')
    date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        db_table = 'user_reps'


class Warn(Model):
    user = ForeignKeyField(User, field='user_id', backref='warns')
    admin = ForeignKeyField(User, field='user_id')
    reason = TextField()
    date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        db_talbe = 'warnings'


class Blacklist(Model):
    phrase = TextField()
    enabled = BooleanField(default=True)

    class Meta:
        database = db


class EntityBlacklist(Model):
    token = CharField(max_length=128)
    token_type = CharField()
    enabled = BooleanField(default=True)

    class Meta:
        database = db

    @hybrid_property
    def full_token(self):
        return f'{self.token} - {self.token_type}'


db.create_tables([Group, Settings, User, Warn, Blacklist, UserLog, Rep,
                  EntityBlacklist])
