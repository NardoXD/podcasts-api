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


