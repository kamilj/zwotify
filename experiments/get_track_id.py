import argparse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def get_track_uris(name):
    client_credentials_manager = SpotifyClientCredentials()
    sp_client = spotipy.Spotify(
        client_credentials_manager=client_credentials_manager)
    sp_client.trace = False

    results = sp_client.search(q='track:' + name, type='track')
    items = results['tracks']['items']
    if len(items) > 0:
        return items

    return None


def main():
    parser = argparse.ArgumentParser(description=(
        """Gets a potential spotify track uri from track title. Results have to be eyeballed to pick the right one based on artist"""))

    parser.add_argument("track_title", type=str)
    args = parser.parse_args()

    outfile = "track_ids.csv"

    tracks = get_track_uris(args.track_title)

    if (tracks is not None):
        with open(outfile, "w") as text_file:
            for track in tracks:
                text_file.write('%s - %s - %s\n' %
                                (track['name'], track['uri'], track['artists'][0]['name']))

        return
    print "Not found"


if __name__ == '__main__':
    main()
