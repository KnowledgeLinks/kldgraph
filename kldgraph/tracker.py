import sys
from datetime import datetime


class Tracker:
    _dot_line_limit = 50

    def __init__(self, summary_interval=10000, dot_interval=1000, use_time=True):
        self.start_time = None
        self.count = 0
        self.dot_interval = dot_interval
        self.summary_interval = summary_interval
        self.use_time = use_time
        self._last_interval = None
        self._dot_line_count = 0

    def start(self):
        self.start_time = datetime.now()
        self._last_interval = self.start_time

    def increment_count(self):
        self.count += 1
        self.check_status()

    def check_status(self):
        if self.count % self.summary_interval == 0 and self.count > 0:
            self.print_summary()
            return
        if self.count % self.dot_interval == 0:
            print('. ', end='', flush=True)
            if self._dot_line_count % self._dot_line_limit == 0 and self._dot_line_count > 0:
                print()
                self._dot_line_count = 0
            self._dot_line_count += 1

    def print_summary(self):
        sys.stdout.write("\n")
        sys.stdout.write("{:,}".format(self.count))
        new_time = datetime.now()
        if self.use_time:
            sys.stdout.write("  Total Time: %s - Interval time: %s - '%s' items per second" %
                             (new_time - self.start_time,
                              new_time - self._last_interval,
                              int(self.count / (new_time - self.start_time).total_seconds())))
        sys.stdout.write("\n")
        self._last_interval = new_time
        self._dot_line_count = 0
