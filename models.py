from peewee import *
from flask_login import UserMixin
import datetime


DATABASE = SqliteDatabase('movies.sqlite')

class Users(UserMixin, Model):
    id = PrimaryKeyField(null=False, unique=True)
    username = CharField(max_length=100)
    email = CharField(max_length=100)
    password = CharField(max_length=100)
    image = CharField(max_length=255)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

class Reviews(Model):
    id = PrimaryKeyField(null=False, unique=True)
    movie_id = CharField(max_length=100)
    created_at = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(Users, backref='movies')
    review = CharField(max_length=255)
    rating = SmallIntegerField()

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Users, Reviews], safe=True)
    print('Tables Created')
    DATABASE.close()