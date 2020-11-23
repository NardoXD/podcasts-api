# Local imports
from extensions import ma


class GenreSchema(ma.Schema):
    class Meta:
        fields = ('genreId', 'name', 'url')


class PodcastSchema(ma.Schema):
    genres = ma.Nested(GenreSchema, many=True)

    class Meta:
        fields = ('id', 'name', 'kind', 'copyright', 'releaseDate',
                  'contentAdvisoryRating', 'url', 'artworkUrl100',
                  'artistName', 'artistId', 'artistUrl', 'genres')


# This Schema is created to not show genre when grouped
class PodcastByGenreSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'kind', 'copyright', 'releaseDate',
                  'contentAdvisoryRating', 'url', 'artworkUrl100',
                  'artistName', 'artistId', 'artistUrl')
