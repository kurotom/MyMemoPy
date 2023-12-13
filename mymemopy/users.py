'''
Anonymous user classes, valid user (valid email).

These classes store different usage limitations per user.
'''

import re
import json
import os


class User:
    '''
    Class main `User`.
    '''

    def load_data(self) -> dict:
        '''
        Loads stored user data.
        '''
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as rdata:
                data = json.load(rdata)
                if data['email'] == self.email:
                    self.type = data['type']
                    self.current_quota = data['current_quota']
                    self.quota_chars_day = data['quota_chars_day']
                    self.timeout = data['timeout']
                    self.last_translate = data['last_translate']
                    self.valid_email = data['valid_email']
                    self.email = data['email']
                    self.key = data['key']
        else:
            self.to_write(data=self.to_dict())

    def to_write(
        self,
        data: dict
    ) -> None:
        '''
        Write data to file JSON.
        '''
        with open(self.filename, 'w', encoding='utf-8') as wdata:
            wdata.write(json.dumps(data))

    def set_quota(
        self,
        quota: int = 0
    ) -> None:
        '''
        Set quota to `User`.
        '''
        if quota > 0:
            new_quota = self.current_quota + quota
            if new_quota <= self.quota_chars_day:
                self.current_quota = new_quota
            else:
                self.current_quota = self.quota_chars_day
            self.to_write(self.to_dict())

    def set_last_translate(
        self,
        time: str
    ) -> None:
        '''
        Set the date of the last use of the translation.
        '''
        self.last_translate = time

    def clear_current_quota(self) -> None:
        '''
        Set to 0 quota chars.
        '''
        self.current_quota = 0
        self.to_write(self.to_dict())

    def get_quota(self) -> None:
        '''
        Set quota chars.
        '''
        return self.current_quota

    def statusQuota(self) -> None:
        '''
        Get quota status.
        '''
        return self.current_quota == self.quota_chars_day

    def to_dict(self) -> dict:
        '''
        Transform `User` data to dict.
        '''
        return {
            'type': self.type,
            'current_quota': self.current_quota,
            'quota_chars_day': self.quota_chars_day,
            'timeout': self.timeout,
            'last_translate': self.last_translate,
            'valid_email': self.valid_email,
            'email': self.email,
            'key': self.key,
        }

    def __str__(self):
        '''
        Representation of object `User`.
        '''
        return 'User: {0}, Usage: {1}, Limit: {2}, Email: {3}'.format(
            self.type,
            self.current_quota,
            self.quota_chars_day,
            self.email
        )


class Anonymous(User):
    '''
    Class to handle users anonymous.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.filename = 'anondata.json'
        self.type = 'Anonymous'
        self.quota_chars_day = 5000
        self.current_quota = 0
        self.timeout = None
        self.last_translate = None
        self.valid_email = False
        self.email = None
        self.key = None


class UserValid(User):
    '''
    Class to handle users valids.
    '''

    def __init__(self, email: str, key: str = None):
        '''
        Constructor
        '''
        self.filename = 'userdata.json'
        self.type = 'UserValid'
        self.quota_chars_day = 50000
        self.current_quota = 0
        self.timeout = None
        self.last_translate = None
        self.valid_email = True
        self.email = self.set_email(email)
        self.key = key

    def set_email(
        self,
        email: str
    ) -> str:
        '''
        Set email.
        '''
        validation = re.match(
                r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,3}$',
                email
            )
        if validation is not None:
            return email
        else:
            raise ValueError('Email invalid.')
