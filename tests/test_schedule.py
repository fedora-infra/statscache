import time
import unittest

import freezegun
import nose.tools


from statscache.schedule import Schedule


class TestSchedule(unittest.TestCase):

    @freezegun.freeze_time('2012-01-14 00:00:00')
    def test_basic(self):
        s = Schedule(minute=[15], hour=[5])
        self.assertEquals(float(s), 5 * 60 * 60 + 15 * 60)

    @freezegun.freeze_time('2012-01-14 12:00:00')
    def test_wrap_day(self):
        s = Schedule(minute=[15], hour=[5])
        self.assertEquals(float(s), 17 * 60 * 60 + 15 * 60)

    @freezegun.freeze_time('2012-01-14 12:15:00')
    def test_wrap_day_match_minute(self):
        s = Schedule(minute=[15], hour=[5])
        self.assertEquals(float(s), 17 * 60 * 60)

    @freezegun.freeze_time('2012-01-14 12:16:00')
    def test_wrap_day_wrap_minute(self):
        s = Schedule(minute=[15], hour=[5])
        self.assertEquals(float(s), 16 * 60 * 60 + 59 * 60)

    @freezegun.freeze_time('2012-01-14 00:00:00')
    def test_working_with_time_sleep(self):
        s = Schedule(second=[1])
        time.sleep(s)  # Let's just make sure this doesn't crash

    @nose.tools.raises(ValueError)
    def test_wrap_invalid_item(self):
        Schedule(minute=['lol'])

    @nose.tools.raises(TypeError)
    def test_wrap_invalid_item_int(self):
        Schedule(minute=1)

if __name__ == '__main__':
    unittest.main()
