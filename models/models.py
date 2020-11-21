from app import db

podcast_genre = db.Table(
    'podcast_genre',
    db.Column('podcastId', db.Integer, db.ForeignKey('podcast.id'), primary_key=True),
    db.Column('genreId', db.Integer, db.ForeignKey('genre.genreId'), primary_key=True)
)


class Podcast(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    kind = db.Column(db.String(50), nullable=False)
    copyright = db.Column(db.String)
    releaseDate = db.Column(db.Date, nullable=False)
    contentAdvisoryRating = db.Column(db.String(50))
    url = db.Column(db.String(1000), nullable=False)
    artworkUrl100 = db.Column(db.String(1000), nullable=False)

    artistName = db.Column(db.String(100), nullable=False)
    artistId = db.Column(db.Integer)
    artistUrl = db.Column(db.String(1000))

    genres = db.relationship('Genre', secondary=podcast_genre)


class Genre(db.Model):
    genreId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    url = db.Column(db.String(1000))


