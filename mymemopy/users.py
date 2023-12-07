'''
Anonymous user classes, valid user (valid email).

These classes store different usage limitations per user.
'''

import re


class User:
    def set_quota(self, quota: int = 0):
        if quota > 0:
            self.current_quota += quota

    def get_quota(self):
        return self.current_quota

    def __str__(self):
        return 'User: {0}, Limit: {1}, Email: {2}'.format(
            self.type,
            self.quota_chars_day,
            self.email
        )


class Anonymous(User):
    def __init__(self):
        self.type = 'Anonymous'
        self.valid_email = False
        self.email = None
        self.quota_chars_day = 5000
        self.current_quota = 0


class UserValid(User):
    def __init__(self, email: str):
        self.type = 'UserValid'
        self.valid_email = True
        self.quota_chars_day = 50000
        self.current_quota = 0
        self.email = self.set_email(email)

    def set_email(
        self,
        email: str
    ) -> str:
        validation = re.match(
                r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,3}$',
                email
            )
        if validation is not None:
            return email
        else:
            raise ValueError('Email invalid.')
