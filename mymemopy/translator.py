'''
Class `MyMemoryTranslate` that handles the translation, shows the supported
languages, returns the translation.
'''

import locale

from mymemopy.utils.languages_support import langs

from mymemopy.utils.time_parse import DatetimeTranslator

from mymemopy.text_wrapper import TextWrapper
from mymemopy.request_api import RequestApi

from mymemopy.users import (
    User,
    Anonymous,
    UserValid
)

from mymemopy.exceptions import (
    ApiGenericException,
    # ApiLimitUsageException,
    ApiAuthUserException,
    ApiLimitUsageException,
    EmptyTextException,
    ParameterErrorException,
    TimeOutUsage
)

from typing import Union


class MyMemoryTranslate:
    '''
    Translate text using Mymemory API.
    '''

    bytes_limit = 500
    line = '-' * 47

    def __init__(
        self,
        user_email: str = None,
        user_key: str = None
    ) -> None:
        '''
        Constructor
        '''
        self.timerCls = DatetimeTranslator()
        self.textwrapper = TextWrapper()
        self.api = RequestApi(timerCls=self.timerCls)
        self.local_lang = locale.getlocale()[0].split('_')[0]
        self.code_langs = list(langs.values())
        self.user = self.__select_user(user_email, user_key)

    def show_languages(
        self,
        all: bool = False
    ) -> None:
        '''
        Print all languages and languages codes supported.
        '''
        s = 0
        e = 10
        items = list(langs.items())

        title = f'\n{"| Language".ljust(38)} | {"Code".ljust(4)} |\n'
        title += self.line
        print(title)

        while True:
            it = items[s:e]
            if it == []:
                break

            for i in it:
                print(f'| {i[0].ljust(36)} | {i[1].ljust(4)} |')

            if all and len(it) % 10 == 0:
                input(self.line)

            s += 10
            e += 10
        print(self.line + '\n')

    def search(
        self,
        lang: str
    ) -> None:
        '''
        Search for matching language.
        '''
        r = []
        for k, v in langs.items():
            if lang.lower() in k.lower():
                r.append([k, v])
        text = ''
        text += self.line + '\n'
        for i in r:
            text += f'| {i[0].ljust(36)} | {i[1].ljust(4)} |\n'
        text += self.line
        print(text)

    def __help(self) -> str:
        '''
        Show help.
        '''
        return '\t    Use `show_languages()` to list all language codes.\n'

    def __send_to_api(
        self,
        data_dict: dict
    ) -> dict:
        '''
        Send data to MyMemory API.

        Returns: dict
            quotaFinished: bool - indicates if it has reached the limit of use.
            result: list - list of string translated.
        '''
        translated_text = []
        source = data_dict['source']
        target = data_dict['target']
        list_translate = data_dict['translate']
        quotaFinished = False
        mean_score = []

        for chunk_text in list_translate:
            response = self.api.get(
                    text=chunk_text,
                    source_lang=source,
                    target_lang=target,
                    email_user=self.user.email,
                    key_user=self.user.key
                )
            if response['quotaFinished']:
                quotaFinished = True

            mean_score.append(float(response['score']))

            translated_text.append(response['translatedText'])

        return {
            'last_translate': self.timerCls.now,
            'quotaFinished': quotaFinished,
            'translated_text': translated_text,
            'mean_score': 0
            # 'mean_score': round(sum(mean_score) / len(mean_score), 2)
        }

    def translate(
        self,
        text: str,
        source_lang: str = 'auto',
        target_lang: str = 'en'
    ) -> Union[dict, None]:
        '''
        Sends the given text to the api. By default, `source_lang` it uses the
        system language (`auto`) and `target_lang` is `en`.

        Returns:
            str: the translated strings.
        '''
        self.__check_timeout_usage(self.user)
        self.__check_quota(self.user)

        if len(text) <= 0:
            raise EmptyTextException()
        else:
            if source_lang == 'auto':
                source_lang = self.local_lang
            else:
                source_lang = source_lang.lower()

            target_lang = target_lang.lower()

            correct_langs = [
                        source_lang in self.code_langs,
                        target_lang in self.code_langs
                    ]
            if not all(correct_langs):
                if correct_langs[0] is False and correct_langs[1] is False:
                    raise ParameterErrorException(
                        f'source_lang="{source_lang}"',
                        f'target_lang="{target_lang}"'
                    )
                elif correct_langs[0] is False:
                    raise ParameterErrorException(
                                f'source_lang="{source_lang}"'
                            )
                elif correct_langs[1] is False:
                    raise ParameterErrorException(
                                f'target_lang="{target_lang}"'
                            )
            else:
                text_wrapper_dict = self.textwrapper.wrap(text)

                data_translate = {
                    'source': source_lang,
                    'target': target_lang,
                    'translate': text_wrapper_dict['result']
                }

                try:
                    res_translate = self.__send_to_api(data_translate)
                    self.user.set_last_translate(
                        time=str(res_translate['last_translate'])
                    )
                    if res_translate['quotaFinished']:
                        self.user.set_quota(self.user.quota_chars_day)
                        return None
                    else:
                        self.user.set_quota(text_wrapper_dict['text_size'])
                        return self.__build_text(
                                    res_translate['translated_text']
                                )

                except ApiLimitUsageException as err1:
                    self.user.timeout = str(self.api.timeout)
                    self.user.to_write(self.user.to_dict())
                    print(err1)
                    return None
                except ApiAuthUserException as err2:
                    self.user.to_write(self.user.to_dict())
                    print(err2)
                    return None
                except ApiGenericException as err3:
                    self.user.to_write(self.user.to_dict())
                    print(err3)
                    return None

    def __build_text(
        self,
        list_data: list
    ) -> str:
        '''
        Build the text and calculate its average score.
        '''
        text = ''
        for line_text in list_data:
            text += line_text
        if text[-1] != '.':
            text += '.'
        return text

    def get_status(self) -> str:
        '''
        Returns status of User.
        '''
        return 'User: {0}, Current quota: {1} Quota limit: {2}'.format(
            self.user.type,
            self.user.current_quota,
            self.user.quota_chars_day,
        )

    def get_quota(self) -> int:
        '''
        Returns quota of characters limit of User.
        '''
        return self.user.get_quota()

    def __select_user(
        self,
        email_user: str = None,
        key_user: str = None
    ) -> User:
        '''
        Initializate User, load data stored of user and return User object.
        '''
        if email_user is None and key_user is None:
            user = Anonymous()
        else:
            user = UserValid(email=email_user, key=key_user)
        user.load_data()
        self.__check_clear_quota(user)
        return user

    def __check_timeout_usage(
        self,
        user: User
    ) -> None:
        '''
        Check whether or not there is an API usage time restriction.

        Raise TimeOutUsage
        '''
        if user.timeout is not None:
            remain_time = self.timerCls.calculate_remain_time(
                                    date_timeout=user.timeout
                                )
            if remain_time is None:
                user.timeout = None
            else:
                user.to_write(user.to_dict())
                raise TimeOutUsage(remain_time)

    def __check_clear_quota(
        self,
        user: User
    ) -> None:
        '''
        Check and reset the API usage counter if it is a different day.
        '''
        if user.last_translate is not None:
            clear_quota_usage = self.timerCls.check_day(
                                        date_string=user.last_translate
                                    )
            if clear_quota_usage:
                user.clear_current_quota()

    def __check_quota(
        self,
        user: User
    ) -> None:
        '''
        Check if `User` has reached the API usage limit.

        Raise ApiLimitUsageException.
        '''
        if user.statusQuota():
            raise ApiLimitUsageException()

    def change_user(
        self,
        user: User = None
    ) -> None:
        '''
        Change User.
        '''
        if user and isinstance(user, User):
            self.user = user
            print(f'Change user to `{self.user.type}`.')

    def __str__(self):
        '''
        Representation of User.
        '''
        return f'{self.user}'
