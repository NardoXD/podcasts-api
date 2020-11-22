import os
import json
from flask import Flask, request
from database import Config, populate_db
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)

# these imports are here because they must to be imported after the SQLAlchemy
# and Marshmallow objects
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


@app.route('/api/search', methods=['GET'])
def search():
    name = request.json['name']
    all_podcasts_by_name = Podcast.query.filter(
        Podcast.name.like(f'%{name}%')
    ).all()

    if len(all_podcasts_by_name) <= 0:
        return {'message': 'Not records with that name were found'}, 404

    return podcasts_schema.jsonify(all_podcasts_by_name)




if __name__ == '__main__':
    app.run()
