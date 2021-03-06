# shows track info for a URN or URL
import sys
import pprint
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

if len(sys.argv) > 1:
    urn = 'spotify:track:%s' % sys.argv[1]
else:
    urn = 'spotify:track:0Svkvt5I79wficMFgaqEQJ'

track = sp.track(urn)
pprint.pprint(track)
