import datetime


class Frequency(object):
    """
    A repeating interval synchronized on an epoch, which defaults to UTC
    midnight of the current day (when this class definiton was loaded).
    """

    # synchronize all frequencies on UTC midnight of current day
    epoch = datetime.datetime.utcnow().replace(hour=0,
                                               minute=0,
                                               second=0,
                                               microsecond=0)

    def __init__(self, interval, epoch=None):
        # synchronize on UTC midnight of the day of creation
        self.interval = interval
        if not isinstance(self.interval, datetime.timedelta):
            raise TypeError("'interval' must be an instance of 'timedelta'")
        self.epoch = epoch or Frequency.epoch
        if not isinstance(self.epoch, datetime.datetime):
            raise TypeError("'epoch' must be an instance of 'datetime'")

    @property
    def days(self):
        return self.interval.days

    @property
    def hours(self):
        return self.interval.seconds // (60*60)

    @property
    def minutes(self):
        return (self.interval.seconds // 60) % 60

    @property
    def seconds(self):
        return self.interval.seconds % 60

    def __str__(self):
        # Pretty-print in the format [[[#d]#h]#m]#s
        s = ''
        if self.days:
            s = str(self.days) + 'd'
        if self.hours:
            s = ''.join([s, str(self.hours), 'h'])
        if self.minutes:
            s = ''.join([s, str(self.minutes), 'm'])
        if self.seconds or not s:
            s = ''.join([s, str(self.seconds), 's'])
        return s

    def __repr__(self):
        kwargs = []
        for (kw, arg) in [('days', self.days),
                          ('hours', self.hours),
                          ('minutes', self.minutes),
                          ('seconds', self.seconds)]:
            if arg:
                kwargs.append('='.join([kw, str(arg)]))
        return ''.join([type(self).__name__, '(', ','.join(kwargs), ')'])

    def time_to_fire(self, now=None):
        """ Get the remaining time-to-fire synchronized on epoch """
        now = now or datetime.datetime.utcnow()
        sec = self.interval.seconds + self.interval.days * 24 * 60 * 60
        diff = now - self.epoch
        rem = sec - (diff.seconds + diff.days * 24 * 60 * 60) % sec
        return datetime.timedelta(seconds=rem - 1,
                                  microseconds=10**6 - now.microsecond)

    def last(self, now=None):
        """ Get the last time-to-fire synchronized on epoch """
        now = now or datetime.datetime.utcnow()
        return self.next(now=now) - self.interval

    def next(self, now=None):
        """ Get the next time-to-fire synchronized on epoch """
        now = now or datetime.datetime.utcnow()
        return now + self.time_to_fire(now=now)

    def __json__(self):
        return self.interval.seconds

    def __float__(self):
        return self.time_to_fire().total_seconds()
