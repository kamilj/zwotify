import sys
import spotipy

''' shows recommendations for the given artist
'''

from spotipy.oauth2 import SpotifyClientCredentials
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False


def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


def show_recommendations_for_artist(artist):
    albums = []
    results = sp.recommendations(seed_artists=[artist['id']])
    for track in results['tracks']:
        print track['name'], '-', track['artists'][0]['name']


artist = get_artist('prince')
if artist:
    show_recommendations_for_artist(artist)
