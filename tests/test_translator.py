
from tests.test_base import TestBase

from mymemopy.users import (
    Anonymous,
    UserValid
)

from tests.samples import texts

from mymemopy.translator import MyMemoryTranslate
from mymemopy.utils.time_parse import DatetimeTranslator
from mymemopy.text_wrapper import TextWrapper
from mymemopy.request_api import RequestApi

from mymemopy.exceptions import (
    ApiGenericException,
    # ApiLimitUsageException,
    ApiAuthUserException,
    ApiLimitUsageException,
    EmptyTextException,
    ParameterErrorException,
    TimeOutUsage
)


class MyMemoryTranslateTestCase(TestBase):

    def setUp(self):
        self.memo = MyMemoryTranslate()

        self.user = Anonymous()
        self.user.current_quota = self.user.quota_chars_day
        self.memoLimited = MyMemoryTranslate()
        self.memoLimited.change_user(self.user)

    def test_empty_test_raise(self):
        with self.assertRaises(EmptyTextException):
            self.memo.translate(
                text="",
                source_lang='es',
                target_lang='en'
            )

    def test_parameter_source_language_wrong(self):
        with self.assertRaises(ParameterErrorException):
            self.memo.translate(
                text=texts.text,
                source_lang='xx',
                target_lang='en'
            )

    def test_parameter_target_language_wrong(self):
        with self.assertRaises(ParameterErrorException):
            self.memo.translate(
                text=texts.text,
                source_lang='es',
                target_lang='xx'
            )
