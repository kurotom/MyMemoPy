'''
Class that is responsible for managing the sending of information to the API,
handles the response and formats it.
'''

import requests

from mymemopy.utils.time_parse import DatetimeTranslator

from mymemopy.exceptions import (
    ApiGenericException,
    ApiLimitUsageException,
    ApiAuthUserException,
)


class RequestApi:
    '''
    Class that handles communication between the application and the API.
    '''
    api_url = 'https://api.mymemory.translated.net'

    def __init__(
        self,
        timerCls: DatetimeTranslator = None
    ) -> None:
        '''
        Constructor.

        Parameters:
            url: str, base url of api.
            timerCls: `DatetimeTranslator`, handles time-related data.
        '''
        self.url = self.api_url
        self.timeout = None
        self.timerCls = timerCls

    def get(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        email_user: str = None,
        key_user: str = None
    ) -> dict:
        '''
        Send the request to the API and return the response or raise an error
        if it occurs.
        '''
        query = f'/get?q={text}&langpair={source_lang}|{target_lang}'
        if key_user is not None:
            query += f'&key={key_user}'
        if email_user is not None:
            query += f'&de={email_user}'

        url = self.url + query

        try:
            response = requests.get(url).json()
        except requests.exceptions.ConnectionError as err1:
            raise ApiGenericException(err1)

        try:
            code_status = int(response['responseStatus'])
        except AttributeError:
            pass

        if code_status == 200:
            return self.__format_response(
                                    data_dict=response
                                )
        elif code_status == 429:
            self.timeout = self.timerCls.parse_date_timeout(
                                response["responseDetails"]
                            )
            raise ApiLimitUsageException()
        elif code_status == 403:
            raise ApiAuthUserException(response["responseDetails"])
            # raise ApiAuthUserException()
        else:
            raise ApiGenericException()

    def __format_response(
        self,
        data_dict: dict
    ) -> dict:
        '''
        Create a dictionary of the response from the API.

        Returns:
             dict : Dictionary with translated text, translation score, list \
                    of matching translations, boolean if quota is reached.
        '''
        translated = data_dict['responseData']
        return {
            'translatedText': translated['translatedText'],
            'score': translated['match'],
            'matches': data_dict['matches'],
            'quotaFinished': data_dict['quotaFinished']
        }
