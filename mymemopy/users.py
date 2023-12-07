'''
Anonymous user classes, valid user (valid email).

These classes store different usage limitations per user.
'''

import re
import json
import os


class User:

    def load_data(self) -> dict:
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as rdata:
                data = json.load(rdata)
                if data['email'] == self.email:
                    self.type = data['type']
                    self.valid_email = data['valid_email']
                    self.current_quota = data['current_quota']
                    self.quota_chars_day = data['quota_chars_day']
                    self.timeout = data['timeout']
                    self.email = data['email']
        else:
            self.to_write(data=self.to_dict())

    def to_write(self, data: dict) -> None:
        with open(self.filename, 'w', encoding='utf-8') as wdata:
            wdata.write(json.dumps(data))

    def set_quota(self, quota: int = 0):
        if quota > 0 and self.current_quota <= self.quota_chars_day:
            self.current_quota += quota
            print(self.to_dict())
            self.to_write(self.to_dict())

    def get_quota(self):
        return self.current_quota

    def statusQuota(self):
        return self.current_quota == self.quota_chars_day

    def to_dict(self):
        return {
            'type': self.type,
            'valid_email': self.valid_email,
            'current_quota': self.current_quota,
            'quota_chars_day': self.quota_chars_day,
            'timeout': self.timeout,
            'email': self.email
        }

    def __str__(self):
        return 'User: {0}, Usage: {1}, Limit: {2}, Email: {3}'.format(
            self.type,
            self.current_quota,
            self.quota_chars_day,
            self.email
        )


class Anonymous(User):

    def __init__(self):
        self.filename = 'anondata.json'
        self.type = 'Anonymous'
        self.valid_email = False
        self.quota_chars_day = 5000
        self.current_quota = 0
        self.timeout = None
        self.email = None


class UserValid(User):

    def __init__(self, email: str):
        self.filename = 'userdata.json'
        self.type = 'UserValid'
        self.valid_email = True
        self.quota_chars_day = 50000
        self.current_quota = 0
        self.timeout = None
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
