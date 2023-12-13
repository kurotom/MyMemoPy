'''
Class to manage times, household items such as: analyzing text looking for
times, converting times, calculating differences, comparing days.
'''

from typing import Union

from datetime import datetime, timedelta
import re


class DatetimeTranslator:
    '''
    Class that manages time-related matters.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.now = datetime.now()

    def parse_date_timeout(
        self,
        data: str
    ) -> Union[timedelta, None]:
        '''
        Find string times using Regex; this time is provided by the API when
        the limit is reached.

        Returns:
            timedelta : calculate disference between `now()` and `timedelta`.
            None : if the Regex match is empty.
        '''
        rgx = r'(\d{2}\sHOURS)\s(\d{2}\sMINUTES)\s(\d{2}\sSECONDS)'
        timeout = re.findall(rgx, data)
        if timeout != []:
            hours, minutes, seconds = timeout[0]
            delta = timedelta(
                hours=int(hours.split(" ")[0]),
                minutes=int(minutes.split(" ")[0]),
                seconds=float(seconds.split(" ")[0]),
            )
            return datetime.now() + delta
        else:
            return None

    def to_datetime(self, string_date: str) -> datetime:
        '''
        Convert string to datetime object.

        Returns:
            datetime
        '''
        return datetime.strptime(string_date, '%Y-%m-%d %H:%M:%S.%f')

    def calculate_remain_time(
        self,
        date_timeout: str
    ) -> Union[datetime, None]:
        '''
        Calculates the remaining time between "now" and the given "time_wait".
        '''
        time_wait = self.to_datetime(date_timeout)
        now = datetime.now()
        if time_wait > now:
            return time_wait - now
        else:
            return None

    def check_day(
        self,
        date_string: str
    ) -> bool:
        '''
        Check if day is different.

        Returns:
            bool : day comparison.
        '''
        time = self.to_datetime(date_string)
        return self.now.day != time.day
