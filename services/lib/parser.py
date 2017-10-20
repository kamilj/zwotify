# -*- coding: utf-8 -*-

import argparse
import xml.etree.ElementTree as ET
import textwrap

from classes.power import Power
from classes.segment import Segment


def round_to_nearest_second(value):
    """ takes a floating point number of seconds as a string and returns
    the number of seconds as an integer """
    return int(round(float(value)))


def parse_power(node):
    if node.tag == "FreeRide":
        return Power(0, 0)

    target_intensity = node.get("Power")
    min_intensity = node.get("PowerLow")
    max_intensity = node.get("PowerHigh")

    if target_intensity is None:
        target_intensity = 0

    if min_intensity is None:
        min_intensity = 0

    if max_intensity is None:
        max_intensity = target_intensity

    return Power(min_intensity, max_intensity)


def parse_interval_power(node, state):
    target_intensity = node.get(state + "Power")
    min_intensity = node.get("Power" + state + "Low")
    max_intensity = node.get("Power" + state + "High")

    if target_intensity is None:
        target_intensity = 0

    if min_intensity is None:
        min_intensity = 0

    if max_intensity is None:
        max_intensity = target_intensity

    return Power(min_intensity, max_intensity)


def convert(input_file):
    """
    """
    # combine very short intervals into at least a 4 minute block
    # because the average track length is 3.5 minutes
    min_interval_set_total_duration = 240
    segments = []
    tree = ET.parse(input_file)
    root = tree.getroot()
    workout = root.find("workout")
    time = 0

    for node in workout:
        if node.tag == "Warmup" \
                or node.tag == "Cooldown" \
                or node.tag == "FreeRide" \
                or node.tag == "SteadyState":
            duration = node.get("Duration")
            cadence = node.get("Cadence")
            end_time = time + round_to_nearest_second(duration)
            power = parse_power(node)
            segments.append(Segment(time, end_time, node.tag, power, cadence))
            time = end_time + 1

        elif node.tag == "IntervalsT":
            repeat = int(node.get("Repeat"))
            on_duration = float(node.get("OnDuration"))
            off_duration = float(node.get("OffDuration"))
            on_power = parse_interval_power(node, "On")
            off_power = parse_interval_power(node, "Off")
            cadence = node.get("Cadence")
            cadence_resting = node.get("CadenceResting")

            interval_total_duration = round_to_nearest_second(
                on_duration) + round_to_nearest_second(off_duration)

            interval_set_total_duration = repeat * interval_total_duration

            if interval_total_duration < min_interval_set_total_duration \
                    or interval_set_total_duration < min_interval_set_total_duration:
                end_time = time + interval_set_total_duration
                segments.append(
                    Segment(time, end_time, node.tag, on_power, cadence))
                time = end_time + 1
            else:
                for interval in range(0, repeat):
                    end_time = time + round_to_nearest_second(on_duration)
                    segments.append(
                        Segment(time, end_time, "%s On %s" % (node.tag, interval), on_power, cadence))
                    time = end_time + 1

                    end_time = time + round_to_nearest_second(off_duration)
                    segments.append(
                        Segment(time, end_time, "%s Off %s" % (node.tag, interval), off_power, cadence_resting))
                    time = end_time + 1

    return segments


def main():
    """ run the module """
    outfile = "segments.txt"

    parser = argparse.ArgumentParser(description=(
        """Converts a Zwift Workout File to array of arguments for Spotify search API"""))

    parser.add_argument(
        "-o",
        "--outfile",
        type=str,
        help="The name of the output file, defauts to segments.txt if none given"
    )

    parser.add_argument("file", type=argparse.FileType('r'))
    args = parser.parse_args()

    if args.outfile != None:
        outfile = args.outfile

    text_file = open(outfile, "w")

    with args.file as file:
        segments = convert(file)
        text_file.write(
            'Type, StartTime, EndTime, Duration, Duration Formatted, Min Intensity, Max Intensity, Tempo)\n')

        for segment in segments:
            text_file.write('%s, %s, %s, %s, %s, %s, %s, %s)\n' % (segment.segment_type, segment.start_time,
                                                                   segment.end_time, segment.duration(), segment.human_duration(), segment.power.min_intensity, segment.power.max_intensity, segment.cadence))


if __name__ == '__main__':
    main()
