'''
Tests base
'''


import unittest

from tests.samples import (
    emails,
    texts
)


class TestBase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestBase, self).__init__(*args, **kwargs)
        self.text = texts.text
        self.emails_valid = emails.valids
        self.emails_invalid = emails.invalids
