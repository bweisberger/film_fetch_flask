from peewee import *
from flask_login import UserMixin
import datetime


DATABASE = PostgresqlDatabase('film_fetch')

class Users(UserMixin, Model):
    id = PrimaryKeyField(null=False, unique=True)
    username = CharField(max_length=100)
    email = CharField(max_length=100)
    password = CharField(max_length=100)
    image = CharField(max_length=255)
    lastWatched = CharField(null=True, max_length=255)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

class History(Model):
    id = PrimaryKeyField(null=False, unique=True)
    movie_id = CharField(max_length=100)
    title = CharField(max_length=255)
    country = CharField(max_length=100)
    created_at = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(Users, backref='history')
    review = CharField(null=True, max_length=255)
    rating = SmallIntegerField(null=True)

    class Meta:
        database = DATABASE
    
class Fellows(Model):
    id = PrimaryKeyField(null=False, unique=True)
    user1 = ForeignKeyField(Users, backref='following')
    user2 = ForeignKeyField(Users, backref="following")

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Users, History, Fellows], safe=True)
    print('Tables Created')
    DATABASE.close()