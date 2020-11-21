import requests


def __fetch_api():
    response = requests.get('https://rss.itunes.apple.com/api/v1/us/podcasts/top-podcasts/all/100/explicit.json')
    results = response.json()['feed']['results']
    return results


def __get_data(results):
    genres_id = set()
    genres = list()

    for podcast in results:
        # Extract genres from each result
        podcast_genres = podcast.get('genres', [])
        for genre in podcast_genres:
            if genre['genreId'] not in genres_id:
                genres_id.add(genre['genreId'])
                genres.append(genre)
    return genres, results


def populate_db(db, Genre, Podcast):
    results = __fetch_api()
    genres, podcasts = __get_data(results)
    genres_dict = {}
    # Save genres on database
    for genre in genres:
        new_genre = Genre(genreId=int(genre['genreId']), name=genre['name'], url=genre['url'])
        genres_dict[genre['genreId']] = new_genre
        db.session.add(new_genre)
        db.session.commit()
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
        # Save podcast
        db.session.add(new_podcast)
        db.session.commit()

        # Add related genres to podcast
        for genre in podcast['genres']:
            new_podcast.genres.append(genres_dict[genre['genreId']])

        db.session.commit()

    print('Database has been populated!!!')
