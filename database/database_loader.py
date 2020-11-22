# Third-party imports
import requests


def __fetch_api():
    """

    :return: all podcasts results of itunes api
    :rtype: list
    """
    response = requests.get(
        'https://rss.itunes.apple.com/api/v1/us/podcasts/top-podcasts/all/100/explicit.json')
    results = response.json()['feed']['results']
    return results


def __get_genres(results):
    """

    :param results: all podcasts results obtained from the itunes api
    :type results: list
    :return: a list of all unique genres stored in the podcasts
    :rtype: list
    """
    genres_id = set()
    genres = list()

    for podcast in results:
        # Extract genres list from each podcast
        podcast_genres = podcast.get('genres', [])

        # for loop to save every unique genre
        for genre in podcast_genres:
            if genre['genreId'] not in genres_id:
                genres_id.add(genre['genreId'])
                genres.append(genre)

    return genres


def populate_db(db, Genre, Podcast):
    """

    :param db: an instance of SQLAlchemy object to manipulate the database
    :param Genre: a Genre model to create new Genre instances
    :param Podcast: a Podcast model to create a new Podcast instances
    :type db: SQLAlchemy object
    :type Genre: Genre object (from models)
    :type Podcast: Podcast object (from models)
    :return: None
    """

    genres_dict = {}

    # Get all podcast from itunes api
    podcasts = __fetch_api()
    # Get all genres from podcasts
    genres = __get_genres(podcasts)

    # Save genres on database
    for genre in genres:
        new_genre = Genre(
            genreId=int(genre['genreId']),
            name=genre['name'],
            url=genre['url']
        )
        # Add genre to genres_dict, this will be used to get the related
        # genres to every podcast
        genres_dict[genre['genreId']] = new_genre

        # Add a new genre to session
        db.session.add(new_genre)

    # Save podcasts with related genres
    for podcast in podcasts:
        new_podcast = Podcast(
            id=int(podcast['id']),
            name=podcast['name'],
            kind=podcast['kind'],
            copyright=podcast.get('copyright', None),
            releaseDate=podcast['releaseDate'],
            contentAdvisoryRating=podcast.get('contentAdvisoryRating', None),
            url=podcast['url'],
            artworkUrl100=podcast['artworkUrl100'],
            artistName=podcast['artistName'],
            artistId=podcast.get('artistId', None),
            artistUrl=podcast.get('artistUrl', None),
        )
        # Add a new podcast to session
        db.session.add(new_podcast)

        # Add related genres to podcast (get genres from genres_dict)
        for genre in podcast['genres']:
            new_podcast.genres.append(genres_dict[genre['genreId']])

    # Make changes in database
    db.session.commit()

    print('Database has been populated!!!')
