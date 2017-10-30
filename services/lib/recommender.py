import os
import sys
import random
import json
import itertools

local_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(local_dir, "./"))

# Outside a virtualenv, sys.real_prefix should not exist.
# if not in virtualenv, then we are running at aws
# and need to get shapely and numpy from the ../lib dir
if not hasattr(sys, 'real_prefix'):
    sys.path.append(os.path.join(local_dir, "./lib"))

import numpy as np
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials
from classes.track_attributes import TrackAttributes


class Recommender:
    def __init__(self,
                 artists=None,
                 tracks=None,
                 genres=None,
                 allow_explicit_lyrics=False,
                 crossfade_duration_seconds=None):
        client_credentials_manager = SpotifyClientCredentials()

        # the max number of seed artists, tracks and genres combined
        self.max_seeds = 5

        self.artists = artists

        self.tracks = tracks

        self.genres = genres

        self.allow_explicit_lyrics = allow_explicit_lyrics

        self.sp_client = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager)
        self.sp_client.trace = False

        self.max_recommendations = 17

        if crossfade_duration_seconds:
            self.crossfade_duration_seconds = crossfade_duration_seconds
        else:
            self.crossfade_duration_seconds = 5

        self.randomize_seed_counts()

    def randomize_seed_counts(self):
        # tracks are the best seeds, so pick 2 to 4 of those
        self.seed_tracks_count = random.randint(2, 4)

        # artists are the next best seeds, so mix in
        # one or more random artists depending on how many seeds slots remain
        self.seed_artists_count = random.randint(
            1, self.max_seeds - self.seed_tracks_count)

        # use genres, only if we have a slots left
        self.seed_genres_count = self.max_seeds - \
            self.seed_tracks_count - self.seed_artists_count

        print ('using %d tracks, %d artist(s),  %d genre(s)' % (
            self.seed_tracks_count, self.seed_artists_count, self.seed_genres_count))

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

        # we are expecting get_track_attrs_for_segment to be called
        # many times for one instance of Recommender,
        # so randomize the seed tracks, artists and genres for each
        # invocation  of this function
        self.randomize_seed_counts()

        attrs = TrackAttributes()

        if self.tracks:
            attrs.tracks = self.sample(self.tracks, self.seed_tracks_count)

        if self.artists:
            attrs.artists = self.sample(self.artists, self.seed_artists_count)

        if self.seed_genres_count:
            attrs.genres = self.sample(self.genres, self.seed_genres_count)

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

    def find_combination(self, choices, total):
        '''
        Subset sum - find the smallest set of
        integers from the choices pool that add up to the total,
        as close as possible without going over.
        https://en.wikipedia.org/wiki/Subset_sum_problem

        @todo - Optimize. This implementation works, but is very slow and uses
        a ton of memory.
        '''
        bins = np.array(
            list(itertools.product([0, 1], repeat=len(choices))))
        combinations = [b for b in bins if sum(choices * b) == total]
        return (min(combinations, key=sum) if combinations else
                max([b for b in bins if sum(choices * b) < total], key=sum))

    def extract_duration_ms(self, json):
        try:
            return json['duration_ms'] - self.crossfade_duration_seconds
        except KeyError:
            return 0

    def get_tracks_for_segment(self, segment):
        attrs = self.get_track_attrs_for_segment(segment)

        # attr_vars = vars(attrs)
        # print ', '.join("%s: %s" % item for item in attr_vars.items())

        segment_duration_ms = segment.duration() * 1000

        print('finding recommendation track(s) to match segment length %s' %
              segment_duration_ms)

        results = self.sp_client.recommendations(
            seed_artists=attrs.artists,
            seed_genres=attrs.genres,
            seed_tracks=None,
            limit=self.max_recommendations,
            country='US',
            target_energy=attrs.energy,
            target_danceability=attrs.danceability,
            target_tempo=attrs.target_tempo,
            target_popularity=attrs.popularity,
            target_duration=attrs.duration_ms
        )

        tracks = results['tracks']

        print ('%d recommendations found.' % len(tracks))

        if (not self.allow_explicit_lyrics):
            print ('Filtering out tracks with explicit lyrics.')

            filtered_tracks = [
                track for track in tracks if not track['explicit']]
            tracks = filtered_tracks

            print ('%d recommendations remaining after filtering.' % len(tracks))

        print ('Arranging tracks to fit workout segment duration.')

        tracks.sort(key=self.extract_duration_ms, reverse=False)

        print ('tracks sorted by duration')

        durations = []

        for track in tracks:
            durations.append(track['duration_ms'])

        # print (durations)

        print ('finding optimal combination of tracks to match segment duration')

        # the combination stores a 0 or 1 in order
        # of the tracks sorted by duration
        # where if we take all the tracks with a 1
        # the sum of the durations is as close as possible
        # to the workout segment length without going over it.
        # e.g. if combination is [0,0,1,1,0] then we pick the
        # tracks at index positions 2,3.
        # The more tracks we request from the recommendations API
        # the more accurately we can match the duration, however,
        # the brute force subset sub alogrithm is pretty slow
        combination = self.find_combination(
            durations, segment_duration_ms)

        print ('optimal combination durations found')

        duration_matched_tracks = []

        total_duration_of_found_tracks = 0

        for x in range(0, len(tracks)):
            if combination[x] == 1:
                total_duration_of_found_tracks += tracks[x]['duration_ms']
                duration_matched_tracks.append(tracks[x])

        print('Needed %d s of music, got %d s, shortfall of %d s\n' % (segment_duration_ms / 1000,
                                                                       total_duration_of_found_tracks / 1000, (segment_duration_ms - total_duration_of_found_tracks) / 1000))

        # todo, keep sum of shortfall

        # for track in duration_matched_tracks:
        #     print track['name'], '-', track['artists'][0]['name']

        # return json.dumps(tracks, indent=4, sort_keys=True)

        return duration_matched_tracks
