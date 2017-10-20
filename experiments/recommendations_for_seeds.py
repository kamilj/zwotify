import sys
import spotipy
import json

''' shows recommendations for the given genres
'''

from spotipy.oauth2 import SpotifyClientCredentials
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False

'''
seed_artists - a list of artist IDs, URIs or URLs
seed_tracks - a list of artist IDs, URIs or URLs
seed_genres - a list of genre names. Available genres for recommendations can be found by calling recommendation_genre_seeds
country - An ISO 3166-1 alpha-2 country code. If provided, all results will be playable in this country.
limit - The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 100
min/max/target_<attribute> - For the tuneable track attributes listed in the documentation, these values provide filters and targeting on results.

'''


def human_time(value):
    """ takes a floating point number of seconds as a string and returns
    a humanly readable time in minutes and seconds """
    seconds = int(round(float(value)))
    if seconds <= 60:
        return "%d secs" % seconds

    mins, secs = divmod(seconds, 60)

    if secs == 0:
        return "%d mins" % mins

    return "%d mins %d secs" % (mins, secs)


results = sp.recommendations(
    seed_artists=None, seed_genres=['electro', 'trance'], seed_tracks=None, limit=20, country='US',
    max_energy=0.6, target_danceability=0.6, target_tempo=120, target_popularity=90
)

# results = sp.recommendations(
#    seed_artists=None, seed_genres=['electro', 'trance'], seed_tracks=None, limit=20, country='US',
#    target_energy=0.7, target_danceability=0.8, min_tempo=80, max_tempo=140, target_valence=0.8, target_popularity=90
#)

# print json.dumps(results)

for track in results['tracks']:
    print '%s - %s - %s' % (track['name'],
                            track['artists'][0]['name'], human_time(track['duration_ms'] / 1000))
