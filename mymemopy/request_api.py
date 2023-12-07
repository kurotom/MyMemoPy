'''
'''

import requests


class RequestApi:
    def __init__(
        self,
        url: str
    ) -> None:
        '''
        Constructor, receives a string corresponding to the api url.
        '''
        self.url = url

    def get(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        email_user: str = None
    ):
        '''
        Send the request to the API and return the response or raise an error
        if it occurs.
        '''
        query = f'/get?q={text}&langpair={source_lang}|{target_lang}'
        if email_user is not None:
            query += f'&de="{email_user}"'

        url = self.url + query
        res = requests.get(url)

        try:
            code_status = int(res.json()['responseStatus'])
        except AttributeError:
            pass

        if code_status == 200:
            return self.__format_response(
                                    data_dict=res.json()
                                )
        elif code_status == 429:
            err_limit = f'Error, characters/day limit reached, {code_status}'
            raise Exception(err_limit)
        elif code_status == 403:
            err_limit = f'Error, email invalid, {code_status}'
            raise Exception(err_limit)
        else:
            err_api = f'Error, receiving responses from API, {res.status_code}'
            raise Exception(err_api)

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
            'matches': data_dict['matches']
        }
