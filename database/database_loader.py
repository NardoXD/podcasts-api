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
