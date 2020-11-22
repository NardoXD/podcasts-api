import os
import json
from flask import Flask, request
from database import Config, populate_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)

# these imports are here because they must to be imported after the SQLAlchemy
# and Marshmallow objects
from models import Podcast, Genre, User
from models import GenreSchema, PodcastSchema, PodcastByGenreSchema

# Schema creation
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)
podcast_schema = PodcastSchema()
podcasts_schema = PodcastSchema(many=True)
podcasts_by_genre_schema = PodcastByGenreSchema()

if 'podcasts.db' not in os.listdir('database/'):
    db.create_all()
    db.session.commit()
    populate_db(db, Genre, Podcast)


@app.route('/api/create-user', methods=['POST'])
def create_user():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username is None:
        return {'message': 'username is required'}, 400
    if password is None:
        return {'message': 'password is required'}, 400

    new_user = User(username, generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    return {'message': 'New user created!'}, 200


@app.route('/api/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return {'message': 'Could not verify!'}, 401

    user = User.query.filter_by(username=auth.username).first()

    if check_password_hash(user.password, auth.password):
        token = User.encode_auth_token(user.id)
        return {'token': token}

    return {'message': 'Could not verify'}, 401


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


@app.route('/api/group-by-genre', methods=['GET'])
def group_by_genre():
    raw_query = """select genre.name as genre, podcast.id as id from genre
join podcast_genre on podcast_genre.genreId = genre.genreId
join podcast on podcast.id == podcast_genre.podcastId
order by genre;"""
    results = db.engine.execute(raw_query).fetchall()

    podcast_by_genre = dict()
    for result in results:
        genre, podcast_id = result
        if genre not in podcast_by_genre.keys():
            podcast_by_genre[genre] = list()

        podcast = Podcast.query.get(podcast_id)
        podcast = podcasts_by_genre_schema.dump(podcast)
        podcast_by_genre[genre].append(podcast)

    return podcast_by_genre, 200


if __name__ == '__main__':
    app.run()
