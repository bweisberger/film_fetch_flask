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
    user = ForeignKeyField(Users, backref='reviews')
    review = CharField(max_length=255)
    rating = SmallIntegerField()

    class Meta:
        database = DATABASE
    
class Amigos(Model):
    id = PrimaryKeyField(null=False, unique=True)
    user1 = ForeignKeyField(Users, backref='following')
    user2 = ForeignKeyField(Users, backref="following")

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Users, Reviews, Amigos], safe=True)
    print('Tables Created')
    DATABASE.close()