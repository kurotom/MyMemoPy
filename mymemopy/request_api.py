'''
'''

import requests

from utils.parsers import parse_date_timeout

from exceptions import (
    ApiGenericException,
    ApiLimitUsageException,
    ApiEmailUserException,
    EmptyTextException,
    ParameterErrorException,
)


class RequestApi:
    def __init__(
        self,
        url: str
    ) -> None:
        '''
        Constructor, receives a string corresponding to the api url.
        '''
        self.url = url
        self.timeout = None

    def get(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        email_user: str = None
    ) -> dict:
        '''
        Send the request to the API and return the response or raise an error
        if it occurs.
        '''
        query = f'/get?q={text}&langpair={source_lang}|{target_lang}'
        if email_user is not None:
            query += f'&de={email_user}'

        url = self.url + query
        response = requests.get(url).json()

        try:
            code_status = int(response['responseStatus'])
        except AttributeError:
            pass

        if code_status == 200:
            return self.__format_response(
                                    data_dict=response
                                )
        elif code_status == 429:
            self.timeout = parse_date_timeout(response["responseDetails"])
            raise ApiLimitUsageException()
        elif code_status == 403:
            raise ApiEmailUserException()
        else:
            raise ApiGenericException()

    def __format_response(
        self,
        data_dict: dict
    ) -> dict:
        '''
        Create a dictionary of the response from the API.
        '''
        translated = data_dict['responseData']
        return {
            'translatedText': translated['translatedText'],
            'score': translated['match'],
            'matches': data_dict['matches'],
            'quotaFinished': data_dict['quotaFinished']
        }
