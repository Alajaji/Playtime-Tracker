import os
import datetime
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
#database_path = "postgres://zzqtmtsfkcduub:5dfa8822c5e8edc7a0ebadc19c9010c963c4b42956bf3efb2297a840f3bb7ee0@ec2-54-172-17-119.compute-1.amazonaws.com:5432/db8uju43bqbbdk"
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Player

'''


class Player(db.Model):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    playtimes = db.relationship('Playtime', backref='Player')

    def __init__(self, name):
        self.name = name

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name
        }


'''
Playtime

'''


class Playtime(db.Model):
    __tablename__ = 'playtime'

    id = Column(Integer, primary_key=True)
    game = Column(String)
    player_id = Column(db.Integer, db.ForeignKey('player.id'))
    playtime = Column(Integer)
    genre = Column(String)

    def __init__(self, game, player_id, playtime, genre):
        self.game = game
        self.player_id = player_id
        self.playtime = playtime
        self.genre = genre

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'game': self.game,
            "playtime_id": self.id,
            'player_id': self.player_id,
            'playtime': str(datetime.timedelta(seconds=self.playtime)),
            'genre': self.genre
        }


'''
Genres

'''


class Genre(db.Model):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, genre):
        self.genre = genre

    def format(self):
        return {
            'id': self.id,
            'name': self.genre
        }
