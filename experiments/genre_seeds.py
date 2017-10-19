import sys
import spotipy
import json


from spotipy.oauth2 import SpotifyClientCredentials
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False

result = sp.recommendation_genre_seeds()

for genre in result['genres']:
    print genre
