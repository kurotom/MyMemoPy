'''
'''

from typing import Union

from datetime import datetime, timedelta
import re


def parse_date_timeout(data: str) -> Union[datetime, None]:
    '''
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


def calculate_remain_time(date_timeout: str) -> Union[datetime, None]:
    '''
    '''
    time_wait = datetime.strftime(date_timeout)
    now = datetime.now()
    if time_wait > now:
        return time_wait - now
    else:
        return None
