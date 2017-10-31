import sys
import json
from os import path

localDir = path.dirname(path.realpath(__file__))
sys.path.append(path.join(localDir, "../lib"))
sys.path.append(path.join(localDir, "../seeds"))

from recommender import Recommender
from classes.power import Power
from classes.segment import Segment


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


def print_results(results):
    for track in results:
        print '\t%s - %s - %s - explicit %s' % (track['name'],
                                                track['artists'][0]['name'], human_time(
            track['duration_ms'] / 1000),
            track['explicit'])

    print '\n\n'
    # print json.dumps(results['tracks'], indent=4, sort_keys=True)
    # print json.dumps(results, indent=4, sort_keys=True)


def main():
    recommender = Recommender()

    #influencer = '..\seeds\mike.json'

    influencer = '..\\seeds\\tribby.json'

    # influencer = '..\seeds\emily.json'

    with open(influencer) as json_data:
        influences = json.load(json_data)
        # print(influences)

    recommender.artists = [a['id'] for a in influences['artists']]

    recommender.tracks = [t['id'] for t in influences['tracks']]

    recommender.genres = influences['genres']

    recommender.allow_explicit_lyrics = True

    print 'Warmup, 10 mins, power 20% - 45%, rpm 90\n'
    segment = Segment(0, 600, "Warmup", Power(0.20, 0.45), 90)
    results = recommender.get_tracks_for_segment(segment)
    print_results(results)

    print 'SteadyState, 15 mins, power 45% - 75%, rpm 90\n'
    segment = Segment(0, 900, "SteadyState", Power(0.45, 0.75), 90)
    results = recommender.get_tracks_for_segment(segment)
    print_results(results)

    print 'IntervalsT, 20 mins, power 75% - 150%, rpm 120\n'
    segment = Segment(0, 1200, "IntervalsT", Power(0.75, 1.5), 90)
    results = recommender.get_tracks_for_segment(segment)
    print_results(results)

    print 'CoolDown, 10 mins, power 25% - 45%, rpm 90\n'
    segment = Segment(0, 600, "CoolDown", Power(0.25, 0.45), 90)
    results = recommender.get_tracks_for_segment(segment)
    print_results(results)


if __name__ == '__main__':
    main()
