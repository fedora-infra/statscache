import datetime
import re


__all__ = ['Schedule', 'Frequency']

# A very small number
EPSILON = 0.00001


class Denomination(object):
    """ A denomination of time """
    def __init__(self, value):
        self.value = list(set(value or self.default))
        self.value.sort()
        for item in self.value:
            if item not in self.default:
                raise ValueError("%r is not allowed" % item)

    def next(self, now, remainder=0):
        T = getattr(now, type(self).__name__.lower()) + remainder
        try:
            return next(v for v in self.value if v >= T), 0
        except StopIteration:
            return next(iter(self.value)), 1

    def prev(self, now, remainder=0):
        _t = getattr(now, type(self).__name__.lower()) - remainder
        _t, remainder = (self.default[-1] + 1, 1) if _t < 0 else (_t, 0)
        try:
            return next(v for v in self.value[::-1] if v <= _t), remainder
        except StopIteration:
            return next(iter(self.value[::-1])), 1


class Second(Denomination):
    default = range(0, 60)


class Minute(Denomination):
    default = range(0, 60)


class Hour(Denomination):
    default = range(0, 24)


class Schedule(object):
    """ An iterable class for repeating, possibly irregular time intervals """
    def __init__(self, second=None, minute=None, hour=None):

        self.check_inputs(second=second, minute=minute, hour=hour)

        # Let higher order denominations precede lesser ones
        # https://github.com/fedora-infra/statscache/issues/10
        second = second or (minute and [0])
        minute = minute or (hour and [0])

        self.second = Second(second)
        self.minute = Minute(minute)
        self.hour = Hour(hour)

    @classmethod
    def check_inputs(cls, **kwargs):
        for key, value in kwargs.items():
            if value == []:
                raise ValueError("Illegal value for %s %r" % (key, value))

    def __iter__(self):
        return self

    def next(self, now=None):
        """ Returns the datetime object representing when we'll fire next. """
        now = now or datetime.datetime.utcnow()
        s, remainder = self.second.next(now, EPSILON)
        m, remainder = self.minute.next(now, remainder)
        h, remainder = self.hour.next(now, remainder)
        return datetime.datetime(now.year, now.month, now.day, h, m, s) + \
            datetime.timedelta(days=remainder)

    def prev(self, now=None):
        """ Returns the datetime object representing when we last fired """
        now = now or datetime.datetime.utcnow()
        s, remainder = self.second.prev(now, EPSILON)
        m, remainder = self.minute.prev(now, remainder)
        if remainder or m != now.minute:
            s, _ = self.second.prev(
                now - datetime.timedelta(seconds=now.second), 1)
        h, remainder = self.hour.prev(now, remainder)
        if remainder or h != now.hour:
            m, _ = self.minute.prev(
                now - datetime.timedelta(seconds=60 * now.minute), 1)
        return datetime.datetime(now.year, now.month, now.day, h, m, s) - \
            datetime.timedelta(days=1 * remainder)

    # For nice rendering
    def __str__(self):
        return str(self.next() - datetime.datetime.utcnow())

    def __repr__(self):
        return "<Schedule, fires next in %s>" % str(self)

    # For serialization
    def __json__(self):
        return float(self)

    # For usage in 'time.sleep(self)'
    def __float__(self):
        """ Return the number of seconds until we should fire next """
        return (self.next() - datetime.datetime.utcnow()).total_seconds()

    def __int__(self):
        return int(float(self))


class Frequency(object):
    """ Similar as Schedule except only for simple, regular time intervals """
    p = re.compile(r'^(?P<value>\d{1,2})(?P<unit>h|m|s)$')

    def __init__(self, s):
        m = self.p.match(s)
        if m is None:
            raise ValueError('%r is not allowed' % s)
        value, unit = m.groups()
        value = int(value)
        self._schedule = None
        if unit in ('s', 'm'):
            if not (value > 0 and value <= 60):
                raise ValueError('%r is not allowed' % s)
            if unit == 's':
                key = 'second'
            else:
                key = 'minute'
            kwargs = {key: range(0, 60, value)}
            self._schedule = Schedule(**kwargs)
        elif unit == 'h':
            if not (value > 0 and value <= 24):
                raise ValueError('%r is not allowed' % s)
            self._schedule = Schedule(hour=range(0, 24, value))
        else:
            raise ValueError('%r is not allowed' % s)
        self._s = s

    def next(self, now=None):
        return self._schedule.next(now)

    def prev(self, now=None):
        return self._schedule.prev(now)

    def __str__(self):
        return str(self._s)

    def __repr__(self):
        return '<Frequency: %s>' % str(self)
