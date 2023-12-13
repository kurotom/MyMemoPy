from tests.test_base import TestBase

from mymemopy.request_api import RequestApi
from mymemopy.utils.time_parse import DatetimeTranslator

from mymemopy.exceptions import (
    ApiGenericException,
    ApiLimitUsageException,
    ApiAuthUserException,
)

from unittest.mock import patch, Mock


class RequestApiTestCase(TestBase):

    def setUp(self):
        self.api = RequestApi(timerCls=DatetimeTranslator())

        self.data_success = {
            "responseData": {
                "translatedText": "hello",
                "match": 0.98
            },
            "quotaFinished": False,
            "mtLangSupported": None,
            "responseDetails": "",
            "responseStatus": 200,
            "responderId": None,
            "exception_code": None,
            "matches": []
        }
        self.limit_quota = {
            "responseData": {
                "translatedText": "",
            },
            "quotaFinished": None,
            "mtLangSupported": None,
            "responseDetails": "MYMEMORY WARNING: YOU USED ALL AVAILABLE FREE \
            TRANSLATIONS FOR TODAY. NEXT AVAILABLE IN  14 HOURS 17 MINUTES 32 \
            SECONDS VISIT HTTPS://MYMEMORY.TRANSLATED.NET/DOC/USAGELIMITS.PHP \
            TO TRANSLATE MORE",
            "responseStatus": 429,
            "responderId": None,
            "exception_code": None,
            "matches": ""
        }
        self.error_email = {
            "responseData": {
                "translatedText": "",
            },
            "quotaFinished": None,
            "mtLangSupported": None,
            "responseDetails": "INVALID EMAIL PROVIDED",
            "responseStatus": "403",
            "responderId": None,
            "exception_code": None,
            "matches": ""
        }
        self.error_key = {
            "responseData": {
                "translatedText": "",
            },
            "quotaFinished": None,
            "mtLangSupported": None,
            "responseDetails": "AUTHENTICATION FAILURE. TIP: DO NOT USE 'KEY' \
            AND 'USER' IF YOU DON'T NEED TO ACCESS YOUR PRIVATE MEMORIES. TO \
            CREATE A VALID ACCOUNT, PLEASE DO THE FOLLOWING: 1) REGISTER AS A \
            TRANSLATOR HERE: HTTPS://TRANSLATED.NET/TOP/ ; 2) GET AN API KEY \
            HERE: HTTPS://MYMEMORY.TRANSLATED.NET/DOC/KEYGEN.PHP",
            "responseStatus": "403",
            "responderId": None,
            "exception_code": None,
            "matches": ""
        }

    @patch('mymemopy.request_api.requests.get')
    def test_success_get(self, mock_api_data):
        mock_api_data.return_value = Mock()
        mock_api_data.return_value.json.return_value = self.data_success
        mock_api_data.return_value.status_code = 200

        result = self.api.get(
            text='text',
            source_lang='es',
            target_lang='en'
        )
        self.assertEqual(type(result), dict)
        self.assertEqual(
            sorted(list(result.keys())),
            sorted(['translatedText', 'score', 'matches', 'quotaFinished'])
        )

    @patch('mymemopy.request_api.requests.get')
    def test_raise_limit_quota_error(self, mock_api_data):
        mock_api_data.return_value = Mock()
        mock_api_data.return_value.json.return_value = self.limit_quota
        mock_api_data.return_value.status_code = 403

        with self.assertRaises(ApiLimitUsageException):
            self.api.get(
                text='text',
                source_lang='es',
                target_lang='en'
            )

    @patch('mymemopy.request_api.requests.get')
    def test_raise_auth_email_error(self, mock_api_data):
        mock_api_data.return_value = Mock()
        mock_api_data.return_value.json.return_value = self.error_email
        mock_api_data.return_value.status_code = 403

        with self.assertRaises(ApiAuthUserException):
            self.api.get(
                text='text',
                source_lang='es',
                target_lang='en'
            )

    @patch('mymemopy.request_api.requests.get')
    def test_raise_auth_key_error(self, mock_api_data):
        mock_api_data.return_value = Mock()
        mock_api_data.return_value.json.return_value = self.error_key
        mock_api_data.return_value.status_code = 403

        with self.assertRaises(ApiAuthUserException):
            self.api.get(
                text='text',
                source_lang='es',
                target_lang='en'
            )
