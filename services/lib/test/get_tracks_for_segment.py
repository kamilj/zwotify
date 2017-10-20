import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

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
    for track in results['tracks']:
        print '%s - %s - %s - explicit %s' % (track['name'],
                                              track['artists'][0]['name'], human_time(
            track['duration_ms'] / 1000),
            track['explicit'])
    print '\n'


def main():
    recommender = Recommender()

    print 'Warmup, power 20% - 45%, rpm 90\n'
    segment = Segment(0, 600, "Warmup", Power(0.20, 0.45), 90)
    results = recommender.get_tracks_for_segment(segment)
    print_results(results)

    print 'SteadyState, power 45% - 75%, rpm 90\n'
    segment = Segment(0, 600, "SteadyState", Power(0.45, 0.75), 90)
    results = recommender.get_tracks_for_segment(segment)
    print_results(results)

    print 'IntervalsT, power 75% - 150%, rpm 120\n'
    segment = Segment(0, 600, "IntervalsT", Power(0.75, 1.5), 120)
    results = recommender.get_tracks_for_segment(segment)
    print_results(results)

    print 'CoolDown, power 25% - 45%, rpm 90\n'
    segment = Segment(0, 600, "CoolDown", Power(0.25, 0.45), 90)
    results = recommender.get_tracks_for_segment(segment)
    print_results(results)


if __name__ == '__main__':
    main()
