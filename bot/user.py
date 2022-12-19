import json
import os.path

USER_PATH = 'data/users.txt'
PREFERENCE_PATH = 'data/preferences/'


class User:
    __username: str
    __id: int
    __preferable_language: str
    __preferable_currency: str

    def __init__(self, username=None, _id=None, js=None):
        if js is None:
            try:
                if not os.path.isfile(USER_PATH):
                    open(USER_PATH, 'x').close()
                if not check_username(_id):
                    add_user(_id, username)
            except OSError as e:
                print(e)

            self.username = username
            self.id = _id
            self.preferable_currency = 'RUB'
            self.preferable_language = 'Russian'
        else:
            self.__dict__ = json.loads(js)

    @property
    def preferable_currency(self):
        return self.__preferable_currency

    @preferable_currency.setter
    def preferable_currency(self, value):
        self.__preferable_currency = value

    @property
    def preferable_language(self):
        return self.__preferable_language

    @preferable_language.setter
    def preferable_language(self, value):
        self.__preferable_language = value

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value: str):
        if value.isspace():
            self.__username = 'NoName'
        else:
            self.__username = value

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    def __repr__(self):
        return self.__dict__.__repr__()


def check_currency(currency: str):
    if currency == "RUB":
        return 'Рубль 🇷🇺'
    elif currency == "USD":
        return 'Доллар 🇺🇸'
    return


def check_username(_id: int):
    with open(USER_PATH, 'r') as f:
        for line in f:
            if f'ID: {_id}' in line:
                return True
    return False


def add_user(_id: int, username: str):
    with open(USER_PATH, 'a') as f:
        f.write(f'[User] => ID: {_id} | {username}\n')


def write_json(user):
    if isinstance(user, User):
        jsoned = json.dumps(user, default=lambda o: o.__dict__,
                            sort_keys=True, indent=4)
        with open(PREFERENCE_PATH + str(user.id) + '.json', 'w+') as f:
            f.write(jsoned)


def read_json(_id: int):
    with open(PREFERENCE_PATH + str(_id) + '.json', 'r') as f:
        class_dict = '\n'.join(f.readlines())
    user = User(js=class_dict)
    return user


def edit_json(_id: int, currency, user):
    user.preferable_currency = currency
    jsoned = json.dumps(user, default=lambda o: o.__dict__,
                        sort_keys=True, indent=4)
    with open(PREFERENCE_PATH + str(_id) + '.json', 'w+') as f:
        f.write(jsoned)
