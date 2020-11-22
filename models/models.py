from uuid import uuid4
import datetime
import jwt
from database import Config
from app import db

podcast_genre = db.Table(
    'podcast_genre',
    db.Column('podcastId', db.Integer, db.ForeignKey('podcast.id'), primary_key=True),
    db.Column('genreId', db.Integer, db.ForeignKey('genre.genreId'), primary_key=True)
)


class Podcast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    kind = db.Column(db.String(50))
    copyright = db.Column(db.String, nullable=True)
    releaseDate = db.Column(db.String(10))
    contentAdvisoryRating = db.Column(db.String(50), nullable=True)
    url = db.Column(db.String(1000))
    artworkUrl100 = db.Column(db.String(1000))

    artistName = db.Column(db.String(100))
    artistId = db.Column(db.Integer, nullable=True)
    artistUrl = db.Column(db.String(1000), nullable=True)

    genres = db.relationship('Genre', secondary=podcast_genre, backref=db.backref('podcasts'))


class Genre(db.Model):
    genreId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    url = db.Column(db.String(1000))


class User(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, password):
        self.id = str(uuid4())
        self.username = username
        self.password = password
        self.registered_on = datetime.datetime.utcnow()

    @staticmethod
    def encode_auth_token(user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    minutes=30),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                Config.SECRET_KEY
            ).decode('UTF-8')
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        payload = jwt.decode(auth_token, Config.SECRET_KEY)
        return payload['sub']
