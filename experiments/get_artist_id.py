import argparse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def get_artist_uri(name):
    client_credentials_manager = SpotifyClientCredentials()
    sp_client = spotipy.Spotify(
        client_credentials_manager=client_credentials_manager)
    sp_client.trace = False

    results = sp_client.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]['uri']

    return None


def main():
    parser = argparse.ArgumentParser(description=(
        """Gets a spotify artist uri from artist name"""))

    parser.add_argument("artist_name", type=str)
    args = parser.parse_args()

    outfile = "artist-seeds.csv"

    artist_uri = get_artist_uri(args.artist_name)

    if (artist_uri is not None):
        line = "%s,%s\n" % (args.artist_name, artist_uri)
        with open(outfile, "a") as text_file:
            text_file.write(line)
        print line
        return
    print "Not found"


if __name__ == '__main__':
    main()
