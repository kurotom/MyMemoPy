'''
Example of use, anonymous user and valid user.
'''

from mymemopy.translator import MyMemoryTranslate


def valid_user():
    vu = MyMemoryTranslate(user_email='example@example.com')
    print(vu)
    print(vu.get_quota())
    res = vu.translate('hola', 'es', 'en')
    print(res)
    print(vu)

def anon_user():
    au = MyMemoryTranslate()
    print(au)
    print(au.get_quota())
    res = au.translate('hola', 'es', 'en')
    print(res)
    print(au)



if __name__ == '__main__':
    anon_user()

    valid_user()
