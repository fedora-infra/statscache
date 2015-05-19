import datetime


__all__ = ['Schedule']

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


class Second(Denomination):
    default = range(0, 60)


class Minute(Denomination):
    default = range(0, 60)


class Hour(Denomination):
    default = range(0, 24)


class Schedule(object):
    def __init__(self, second=None, minute=None, hour=None):
        self.second = Second(second)
        self.minute = Minute(minute)
        self.hour = Hour(hour)

    def __iter__(self):
        return self

    def next(self):
        """ Returns the datetime object representing when we'll fire next. """
        now = datetime.datetime.utcnow()
        s, remainder = self.second.next(now, EPSILON)
        m, remainder = self.minute.next(now, remainder)
        h, remainder = self.hour.next(now, remainder)
        return datetime.datetime(now.year, now.month, now.day, h, m, s) + \
            datetime.timedelta(days=remainder)

    # For nice rendering
    def __str__(self):
        return str(self.next() - datetime.datetime.utcnow())

    def __repr__(self):
        "<Schedule, fires next in %s>" % str(self)

    # For serialization
    def __json__(self):
        return float(self)

    # For usage in 'time.sleep(self)'
    def __float__(self):
        """ Return the number of seconds until we should fire next """
        value = (self.next() - datetime.datetime.utcnow()).total_seconds()
        print "Returning", value
        return value

    def __int__(self):
        return int(float(self))
