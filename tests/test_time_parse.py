
from datetime import datetime, timedelta

from tests.test_base import TestBase

from mymemopy.utils.time_parse import DatetimeTranslator


class DatetimeTranslatorTestCase(TestBase):

    def setUp(self):
        self.time = DatetimeTranslator()

    def test_parse_date_timeout(self):
        string = "14 HOURS 17 MINUTES 32 SECONDS"
        s = self.time.parse_date_timeout(data=string)
        self.assertEqual(type(s), datetime)

    def test_calculate_remain_time(self):
        data = self.time.calculate_remain_time(
            str(self.time.now + timedelta(hours=1))
        )
        self.assertEqual(type(data), timedelta)
