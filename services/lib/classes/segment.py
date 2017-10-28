import json


class Segment:
    def __init__(self, start_time, end_time, segment_type, power, cadence=None, working=False):
        self.start_time = start_time
        self.end_time = end_time
        self.segment_type = segment_type
        self.working = working
        self.power = power
        self.duration_ms = (end_time - start_time) * 1000

        if cadence is None:
            self.cadence = 0
        else:
            self.cadence = cadence

    def duration(self):
        return self.end_time - self.start_time

    def human_duration(self):
        """ takes a floating point number of seconds as a string and returns
        a humanly readable time in minutes and seconds """
        seconds = self.duration()
        if seconds <= 60:
            return "%d secs" % seconds

        mins, secs = divmod(seconds, 60)

        if secs == 0:
            return "%d mins" % mins

        return "%d mins %d secs" % (mins, secs)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
