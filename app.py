import os
from flask import Flask
from database import Config, populate_db
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Podcast, Genre
from models import GenreSchema, PodcastSchema, PodcastByGenreSchema

# Schema creation
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)
podcast_schema = PodcastSchema()
podcasts_schema = PodcastSchema(many=True)
podcasts_genre_schema = PodcastByGenreSchema(many=True)

if 'podcasts.db' not in os.listdir('database/'):
    db.create_all()
    db.session.commit()
    populate_db(db, Genre, Podcast)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
