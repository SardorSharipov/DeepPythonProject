import json
import os
import re

GOAL_PATH = 'data/goals/'


class Goal:
    __name: str
    __price: float
    __currency: str
    __user_id: int

    def __init__(self, name: str = 'noname',
                 price: float = 0.0,
                 currency: str = 'RUB',
                 user_id: int = 0,
                 js: str = None
                 ):
        if js is None:
            self.__name = name
            self.__price = price
            self.__currency = currency
            self.__user_id = user_id
        else:
            self.__dict__ = json.loads(js)

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        self.__price = value

    @property
    def currency(self):
        return self.__currency

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        self.__user_id = value

    def __repr__(self):
        return self.__dict__.__repr__()


def write_goal(goal):
    print(isinstance(goal, Goal))
    if isinstance(goal, Goal):
        jsoned = json.dumps(goal, default=lambda o: o.__dict__,
                            sort_keys=True, indent=4)
        with open(GOAL_PATH + str(goal.user_id) + '.json', 'w+') as f:
            f.write(jsoned)


def read_goal(_id: int):
    with open(GOAL_PATH + str(_id) + '.json', 'r') as f:
        class_dict = '\n'.join(f.readlines())
    goal = Goal(js=class_dict)
    return goal


def check_goal(goal):
    if goal.price <= 0:
        delete_goal(goal.user_id)
        return (True, "*Поздравляю 🎉*\n\n" +
                f"Вы накопили свои сбережения и теперь можете приобрести *{goal.name}*")
    else:
        write_goal(goal)
        return (False, f"*Сбережения обновлены 📊*\n\nНа данный момент Вам осталось " +
                f"*{goal.price} {goal.currency}*\n\n" +
                "*Не останавливайтесь, Вы почти у цели!*")


def delete_goal(_id: int):
    os.remove(f"{GOAL_PATH}{_id}.json")


def goal_parser(message: str):
    product_cost = 0
    product_currency = 'RUB'

    parsed_input = re.sub('\s+', ' ', message).split(' ')
    price_index = -1

    for i, parsed in enumerate(parsed_input):
        try:
            product_cost = float(parsed)
            price_index = i
        except:
            pass
    if price_index < 1 or product_cost <= 0:
        return None

    product_name = ' '.join(parsed_input[:price_index])
    return Goal(product_name, product_cost, product_currency)


def has_goal(_id: int):
    return os.path.exists(f'{GOAL_PATH}/{_id}.json')
