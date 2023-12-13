
from tests.test_base import TestBase

from mymemopy.users import (
    User,
    Anonymous,
    UserValid
)


class UserTestCase(TestBase):

    def setUp(self):
        self.anon = Anonymous()
        self.userval = UserValid(self.emails_valid[0])

    def test_data_dict(self):
        data = self.anon.to_dict()
        self.assertEqual(type(data), dict)

    def test_validation_valid_email(self):
        data = [
            self.userval.set_email(dir_email)
            for dir_email in self.emails_valid
        ]
        self.assertTrue(all(data))

    def test_validation_invalid_email(self):
        with self.assertRaises(ValueError):
            for email in self.emails_invalid:
                self.userval.set_email(email)

    def test_get_quota(self):
        self.assertEqual(type(self.anon.get_quota()), int)

    def test_statusQuota(self):
        self.assertEqual(type(self.anon.statusQuota()), bool)
