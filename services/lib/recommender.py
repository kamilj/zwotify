import random
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials
from classes.track_attributes import TrackAttributes


class Recommender:
    def __init__(self,
                 artists=None,
                 max_artists=None,
                 tracks=None,
                 max_tracks=None,
                 genres=None,
                 max_genres=None):
        client_credentials_manager = SpotifyClientCredentials()

        self.artists = artists

        if max_artists is None:
            self.max_artists = 2
        else:
            self.max_artists = max_artists

        self.tracks = tracks

        if max_tracks is None:
            self.max_tracks = 2
        else:
            self.max_tracks = max_tracks

        self.genres = genres

        if max_genres is None:
            self.max_genres = 1
        else:
            self.max_genres = max_genres

        self.sp_client = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager)
        self.sp_client.trace = True

    def sample(self, iterable, n):
        """
        Knuth's Reservoir Sampling (Algorithm R)
        Returns @param n random items from @param iterable.
        https://stackoverflow.com/questions/2612648/reservoir-sampling
        http://data-analytics-tools.blogspot.com/2009/09/reservoir-sampling-algorithm-in-perl.html
        """
        reservoir = []
        for t, item in enumerate(iterable):
            if t < n:
                reservoir.append(item)
            else:
                m = random.randint(0, t)
                if m < n:
                    reservoir[m] = item
        return reservoir

    def get_track_attrs_for_segment(self, segment):
        '''
        https://developer.spotify.com/web-api/get-recommendations/
        '''
        attrs = TrackAttributes()

        if self.artists:
            attrs.artists = self.sample(self.artists, self.max_artists)

        if self.tracks:
            attrs.tracks = self.sample(self.tracks, self.max_tracks)

        if self.genres:
            attrs.genres = self.sample(self.genres, self.max_genres)

        # cadence is not a good selector when used directly
        # but sub-divisions of 4/4, that fit the tempo still work.
        # For example 120 bpm still works for 90 RPM because
        # 12 pedal strokes at 90 rpm match 3 bars of 120 tempo 4/4 time signature

        if (segment.cadence is not None):
            if segment.cadence > 120:
                attrs.target_tempo = 138
            elif segment.cadence >= 90:
                attrs.target_tempo = 120
            elif segment.cadence > 60:
                attrs.target_tempo = 90
            elif segment.cadence >= 58:
                # 60 bpm would suck, double time
                attrs.target_tempo = 120
            elif segment.cadence >= 45:
                attrs.target_tempo = 90

        # randomize popularity starting point between 50% and 100%
        attrs.popularity = random.randrange(50, 100)

        if (segment.duration() is not None):
            attrs.duration_ms = segment.duration() * 1000

        if segment.segment_type == "Warmup":
            # happyish, we're warming up
            attrs.valence = random.uniform(0.7, 0.9)
            # ignore power, get energy going
            attrs.energy = random.uniform(0.65, 0.95)
            if (segment.power.max_intensity is not None):
                attrs.energy = min(segment.power.max_intensity, 0.75)

        elif segment.segment_type == "CoolDown":
            # euphoric, we're done
            attrs.valence = random.uniform(0.85, 0.95)
            # ignore power, high energy celebration
            attrs.energy = random.uniform(0.8, 0.9)

        elif segment.segment_type == "FreeRide" \
                or segment.segment_type == "SteadyState":
            attrs.valence = random.uniform(0.6, 9)
            if (segment.power.max_intensity is not None):
                attrs.energy = min(segment.power.max_intensity, 0.9)
            else:
                attrs.energy = random.uniform(0.8, 0.9)  # cooking

        elif segment.segment_type == "IntervalsT":
            attrs.valence = random.uniform(0.8, 0.9)
            if (segment.power.max_intensity is not None):
                attrs.energy = min(segment.power.max_intensity, 1)
            else:
                attrs.energy = random.uniform(0.85, 1)  # working!

        return attrs

    def get_tracks_for_segment(self, segment):
        attrs = self.get_track_attrs_for_segment(segment)

        # attr_vars = vars(attrs)
        # print ', '.join("%s: %s" % item for item in attr_vars.items())

        results = self.sp_client.recommendations(
            seed_artists=attrs.artists,
            seed_genres=attrs.genres,
            seed_tracks=None,
            limit=10,
            country='US',
            target_energy=attrs.energy,
            target_danceability=attrs.danceability,
            target_tempo=attrs.target_tempo,
            target_popularity=attrs.popularity,
            target_duration=attrs.duration_ms
        )

        return results
