from uuid import uuid4
import datetime
import jwt
from app import app, db, bcrypt

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
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.registered_on = datetime.datetime.now()

    @staticmethod
    def encode_auth_token(user_id):
        try:
            payload = {
                'exp': datetime.datetime.now() + datetime.timedelta(hours=5),
                'iat': datetime.datetime.now(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET__KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again'
        except jwt.InvalidTokenError:
            return 'Invalid token, Please log in again'
