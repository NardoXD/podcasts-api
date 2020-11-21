import requests


def __fetch_api():
    response = requests.get('https://rss.itunes.apple.com/api/v1/us/podcasts/top-podcasts/all/100/explicit.json')
    results = response.json()['feed']['results']
    return results


