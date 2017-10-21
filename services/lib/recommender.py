import random
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials
from classes.track_attributes import TrackAttributes


class Recommender:
    def __init__(self):
        # self.steady_state_seed_artists = ['spotify:artist:3yDIp0kaq9EFKe07X1X2rz',  # Nile Rodgers
        #                                   'spotify:artist:0Xf8oDAJYd2D0k3NLI19OV',  # Chic
        #                                   'spotify:artist:6h3rSZ8VLK7a5vXjEmhfuD',  # The Brothers Johnson
        #                                   'spotify:artist:6gkWznnJkdkwRPVcmnrays',  # Sister Sledge
        #                                   'spotify:artist:3VNITwohbvU5Wuy5PC6dsI'  # Kool & The Gang
        #                                   ]

        self.steady_state_seed_artists = ['3yDIp0kaq9EFKe07X1X2rz',
                                          '6h3rSZ8VLK7a5vXjEmhfuD',
                                          '3VNITwohbvU5Wuy5PC6dsI']

    def get_track_attrs_for_segment(self, segment):
        '''
        https://developer.spotify.com/web-api/get-recommendations/
        '''
        attrs = TrackAttributes()

        if segment.segment_type == "Warmup":

            attrs.speechiness = 3
            attrs.danceability = random.uniform(0.55, 0.7)
            attrs.valence = random.uniform(
                0.7, 0.8)  # happyish, we're waking up
            attrs.popularity = random.randrange(75, 90)
            attrs.genres = ['trance', 'trip-hop', 'electro', 'pop']
            # ignore power, get energy going
            attrs.energy = random.uniform(0.65, 0.95)

            if (segment.power.max_intensity is not None):
                attrs.energy = segment.power.max_intensity

        elif segment.segment_type == "CoolDown":
            attrs.danceability = random.uniform(0.85, 1)
            attrs.valence = random.uniform(0.85, 0.95)  # euphoric, we're done
            # ignore power, high energy celebration
            attrs.energy = random.uniform(0.8, 0.9)
            attrs.popularity = random.randrange(75, 99)
            attrs.genres = ['funk', 'disco', 'breakbeat', 'house', 'dance']

        elif segment.segment_type == "FreeRide" \
                or segment.segment_type == "SteadyState":
            # @todo, switch seed artists based on taste selection
            attrs.artists = self.steady_state_seed_artists
            attrs.genres = None
            attrs.valence = random.uniform(0.67, 0.78)
            attrs.popularity = random.randrange(85, 90)
            if (segment.power.max_intensity is not None):
                attrs.energy = segment.power.max_intensity
            else:
                attrs.energy = random.uniform(0.8, 0.9)  # cooking

        elif segment.segment_type == "IntervalsT":
            attrs.popularity = random.randrange(55, 90)
            attrs.danceability = random.uniform(0.87, 0.95)
            attrs.valence = random.uniform(0.8, 0.9)
            if (segment.power.max_intensity is not None):
                attrs.energy = segment.power.max_intensity
            else:
                attrs.energy = random.uniform(0.9, 1)  # working!

            attrs.genres = ['work-out', 'dance',
                            'power-pop', 'rock', 'metal-misc']

        if (segment.cadence is not None):
            if segment.cadence > 120:
                attrs.target_tempo = 138
            elif segment.cadence > 90:
                attrs.target_tempo = 120
            elif segment.cadence > 60:
                attrs.target_tempo = 80
            elif segment.cadence > 60:
                attrs.target_tempo = 80

        if (segment.duration() is not None):
            attrs.duration_ms = segment.duration() * 1000

        return attrs

    def get_tracks_for_segment(self, segment):
        client_credentials_manager = SpotifyClientCredentials()
        sp_client = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager)
        sp_client.trace = False

        attrs = self.get_track_attrs_for_segment(segment)

        attr_vars = vars(attrs)
        print ', '.join("%s: %s" % item for item in attr_vars.items())

        results = sp_client.recommendations(
            seed_artists=attrs.artists, seed_genres=attrs.genres,
            seed_tracks=None,
            limit=20,
            country='US',
            target_energy=attrs.energy,
            target_danceability=attrs.danceability,
            target_tempo=attrs.target_tempo,
            target_popularity=attrs.popularity,
            target_duration=attrs.duration_ms
        )

        return results
