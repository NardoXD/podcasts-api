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


@app.route('/api/top-20', methods=['POST'])
def save_top_20():
    top_20 = Podcast.query.order_by(Podcast.id).limit(20).all()
    top_20 = podcasts_schema.dump(top_20)
    with open('files/top_20.json', 'w') as file:
        json.dump(top_20, file)

    return {
        'message': 'Top 20 of podcasts has been written in files/top_20.json'
    }, 200


@app.route('/api/replace-top-20', methods=['POST'])
def replace_top_20():
    bottom_20 = Podcast.query.order_by(db.desc(Podcast.id)).limit(20).all()
    bottom_20 = podcasts_schema.dump(bottom_20)
    with open('files/top_20.json', 'w') as file:
        json.dump(bottom_20, file)

    return {
        'message': 'Top 20 has been replaced for Bottom 20 in files/top_20.json'
    }, 200


@app.route('/api/<id_>', methods=['DELETE'])
def delete_podcast(id_):
    podcast = Podcast.query.get(id_)
    if podcast is None:
        return {'message': f'Podcast with id {id_} does not exist'}, 404

    db.session.delete(podcast)
    db.session.commit()

    return {
        'message': f'Podcast with id {id_} has been deleted'
    }, 200


if __name__ == '__main__':
    app.run()
