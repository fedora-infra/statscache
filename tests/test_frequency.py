import time
import unittest

import freezegun
import nose.tools


from datetime import datetime, timedelta
from statscache.frequency import Frequency

def midnight_of(day):
    return day.replace(hour=0, minute=0, second=0, microsecond=0)

class TestFrequency(unittest.TestCase):

    @freezegun.freeze_time('2012-01-14 00:00:00')
    def test_basic(self):
        now = datetime.now()
        f = Frequency(timedelta(minutes=15, hours=5), midnight_of(now))
        self.assertEquals(f.time_to_fire(now=now).total_seconds(),
                          (5 * 60 + 15) * 60)

    @freezegun.freeze_time('2012-01-14 00:00:00')
    def test_one_second(self):
        now = datetime.now()
        f = Frequency(timedelta(seconds=1), midnight_of(now))
        self.assertEquals(f.time_to_fire(now=now).total_seconds(), 1)

    @freezegun.freeze_time('2012-01-14 00:00:01')
    def test_one_second_ahead(self):
        now = datetime.now()
        f = Frequency(timedelta(seconds=1), midnight_of(now))
        self.assertEquals(f.time_to_fire(now=now).total_seconds(), 1)

    @freezegun.freeze_time('2012-01-14 00:00:00')
    def test_two_seconds(self):
        now = datetime.now()
        f = Frequency(timedelta(seconds=2), midnight_of(now))
        self.assertEquals(f.time_to_fire(now=now).total_seconds(), 2)

    @freezegun.freeze_time('2012-01-14 00:00:00')
    def test_working_with_time_sleep(self):
        now = datetime.now()
        f = Frequency(timedelta(seconds=1), midnight_of(now))

        value = f.time_to_fire(now=now).total_seconds()
        # Be careful not to sleep for 20 years if there's a bug
        if value > 2:
            raise ValueError("sleeping too long %r" % value)

        time.sleep(f)  # Let's just make sure this doesn't crash

    @freezegun.freeze_time('2012-01-14 04:00:00')
    def test_last_before_epoch(self):
        now = datetime.now()
        f = Frequency(timedelta(minutes=15, hours=5), now)
        self.assertEquals(f.last(now=(now - timedelta(seconds=1))),
            datetime(year=2012, month=1, day=13, hour=22, minute=45))

    @freezegun.freeze_time('2012-01-14 05:19:27')
    def test_last_on_epoch(self):
        now = datetime.now()
        f = Frequency(timedelta(hours=5, minutes=20, seconds=30), midnight_of(now))
        self.assertEquals(f.last(now=now), datetime(year=2012, month=1, day=14))

    @nose.tools.raises(TypeError)
    def test_invalid_interval(self):
        Frequency('banana', datetime.utcnow())

    @nose.tools.raises(TypeError)
    def test_invalid_epoch(self):
        Frequency(timedelta(seconds=15), 'squirrels')


class TestFrequencyString(unittest.TestCase):

    def test_second(self):
        f = Frequency(timedelta(seconds=10), datetime.utcnow())
        self.assertEqual(str(f), '10s')

    def test_minute(self):
        f = Frequency(timedelta(minutes=10), datetime.utcnow())
        self.assertEqual(str(f), '10m')

    def test_hour(self):
        f = Frequency(timedelta(hours=1), datetime.utcnow())
        self.assertEqual(str(f), '1h')

    def test_hour(self):
        f = Frequency(timedelta(days=1), datetime.utcnow())
        self.assertEqual(str(f), '1d')

    def test_all(self):
        f = Frequency(timedelta(days=1, hours=1, minutes=1, seconds=1),
                      datetime.utcnow())
        self.assertEqual(str(f), '1d1h1m1s')


if __name__ == '__main__':
    unittest.main()
