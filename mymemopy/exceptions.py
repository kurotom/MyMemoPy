'''
Exceptions used in the application.
'''

from terminal_in_colors import ColorTerminal
from requests import RequestException
from datetime import datetime


def color(
    text: str,
    colorname: str,
    isbold: bool
) -> str:
    c = ColorTerminal()
    return c.paint(
        string=text,
        color=colorname,
        bold=isbold,
    )


class ApiGenericException(RequestException):
    '''
    Class base of exception for general errors of comunication to the API.
    '''
    code = None

    def __init__(self, message: str = None):
        if message is None:
            self.message = 'Error, receiving responses from API.'
        else:
            self.message = message
        super().__init__(
                color(text=self.message, colorname='red', isbold=True)
            )


class ApiLimitUsageException(RequestException):
    '''
    Class exception due to API usage limit reached.
    '''
    code = 429

    def __init__(self, message: str = None):
        if message is None:
            self.message = 'Error, characters/day limit reached, {0}'.format(
                color(text=str(self.code), colorname='red', isbold=True)
                )
        else:
            self.message = message
        super().__init__(self.message)


class ApiAuthUserException(RequestException):
    '''
    Class exception when using an invalid email.
    '''
    code = 403

    def __init__(self, message: str = None):
        if message is None:
            self.message = 'Error, email invalid, {0}'.format(
                color(text=str(self.code), colorname='red', isbold=True)
            )
        else:
            self.message = message
        super().__init__(self.message)


class EmptyTextException(Exception):
    '''
    Class exception for texto or string is empty.
    '''
    def __init__(self, message: str = None):
        if message is None:
            self.message = 'The "text" parameter must be at least 1 character.'
        else:
            self.message = message
        super().__init__(
                color(text=self.message, colorname='red', isbold=True)
            )


class ParameterErrorException(Exception):
    '''
    Class exception for given parameters are wrong.
    '''
    def __init__(self, *args):
        params = ', '.join(list(map(str, args)))
        self.message = '\n\tParameter incorrect: '
        self.message += color(text=str(params), colorname='red', isbold=True)
        super().__init__(self.message)


class TimeOutUsage(Exception):
    '''
    Class exception if api use timeout exists.
    '''
    def __init__(self, timeout: datetime):
        self.message = 'Remaining waiting time: {0}'.format(
            color(text=str(timeout), colorname='red', isbold=True)
        )
        super().__init__(self.message)
