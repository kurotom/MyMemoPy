
from tests.test_base import TestBase

from mymemopy.text_wrapper import TextWrapper

from tests.samples import (
    texts
)


class TextWrapperTestCase(TestBase):

    def setUp(self):
        self.wrap = TextWrapper()

    def test_wrap(self):
        res = self.wrap.wrap(text=texts.text)
        self.assertEqual(type(res), dict)
