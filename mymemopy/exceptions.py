from requests import RequestException
from datetime import datetime


class ApiGenericException(RequestException):
    code = None

    def __init__(self):
        self.message = 'Error, receiving responses from API.'
        super().__init__(self.message)


class ApiLimitUsageException(RequestException):
    code = 429

    def __init__(self):
        self.message = f'Error, characters/day limit reached, {self.code}'
        super().__init__(self.message)


class ApiEmailUserException(RequestException):
    code = 403

    def __init__(self, ):
        self.message = f'Error, email invalid, {self.code}'
        super().__init__(self.message)


class EmptyTextException(Exception):
    def __init__(self):
        self.message = 'The "text" parameter must be at least 1 character.'
        super().__init__(self.message)


class ParameterErrorException(Exception):
    def __init__(self, *args):
        params = list(map(str, args))
        self.message = '\n\tParameter incorrect: ' + ', '.join(params)
        super().__init__(self.message)


class TimeOutUsage(Exception):
    def __init__(self, timeout: datetime):
        self.message = f'Remaining waiting time: {timeout}'
        super().__init__(self.message)
