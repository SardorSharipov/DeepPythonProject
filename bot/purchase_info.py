import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from typing import List

PURCHASE_PATH = "data/purchases/"


@dataclass
class PurchaseInfo:
    date: datetime
    obj: str
    price: float
    currency: str
    type_: str

    def __repr__(self):
        return f'{self.obj.replace("_", "").replace("`", "").replace("*", "")} ' \
               f'{self.price}₽ ' \
               f'{self.type_.replace("_", "").replace("`", "").replace("*", "")} ' \
               f'{self.date.strftime("%d-%m-%Y")}'


def write_purchase(id_: int, purchase: PurchaseInfo):
    def json_default(value):
        if isinstance(value, datetime):
            return dict(year=value.year, month=value.month, day=value.day)
        else:
            return value.__dict__

    purchases = []
    if os.path.exists(f'{PURCHASE_PATH}{id_}.json'):
        purchases = read_purchase(id_)
    purchases.append(purchase)
    jsoned = json.dumps({'purchases': purchases}, default=json_default,
                        sort_keys=True, indent=4)
    with open(f'{PURCHASE_PATH}{id_}.json', 'w+') as f:
        f.write(jsoned)
        print('success write purchase')


def read_purchase(id_: int):
    with open(f'{PURCHASE_PATH}{id_}.json', 'r') as f:
        class_dict = '\n'.join(f.readlines())
    classes = json.loads(class_dict)
    purchases = []
    for js in classes['purchases']:
        purchase = PurchaseInfo(datetime.now(), '', 0, 'RUB', 'Разное')
        purchase.currency = js['currency']
        purchase.obj = js['obj']
        purchase.price = js['price']
        purchase.type_ = js['type_']
        purchase.date = datetime(js['date']['year'], js['date']['month'], js['date']['day'])
        purchases.append(purchase)
    return purchases


def delete_purchase(id_: int, number: int):
    purchases = read_purchase(id_)
    if len(purchases) < number or number <= 0:
        raise ValueError()
    purchases = purchases[:number] + purchases[number:]
    jsoned = json.dumps({'purchases': purchases}, default=lambda o: o.__dict__,
                        sort_keys=True, indent=4)
    with open(f'{PURCHASE_PATH}{id}.json', 'w+') as f:
        f.write(jsoned)


def delete_purchases(id_: int, left_border: int, right_border: int):
    purchases = read_purchase(id_)
    if len(purchases) < right_border or left_border <= 0 or \
            right_border <= 0 or right_border < left_border:
        raise ValueError()
    purchases = purchases[:left_border] + purchases[right_border + 1:]
    jsoned = json.dumps({'purchases': purchases}, default=lambda o: o.__dict__,
                        sort_keys=True, indent=4)
    with open(f'{PURCHASE_PATH}{id_}.json', 'w+') as f:
        f.write(jsoned)


def purchase_parsing(message: str, _: int):
    product_cost = 0
    product_currency = 'RUB'
    product_date = datetime.now()

    parsed_input = re.sub("\s+", " ", message).split(' ')
    print(f'parsed_input: {parsed_input}')
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
    date_index = -1
    for i, parsed in enumerate(parsed_input):
        try:
            product_date = datetime.strptime(parsed, "%d-%m-%Y")
            date_index = i
        except:
            pass

    currency_index = price_index
    if price_index != len(parsed_input) - 1:
        if re.search("^руб.*$", parsed_input[currency_index + 1]):
            currency_index += 1
            product_currency = "RUB"
    product_type = ''
    if currency_index != price_index and date_index != -1 and currency_index != date_index - 1:
        for i in range(currency_index + 1, date_index):
            product_type += parsed_input[i] + ' '
    elif currency_index == price_index and date_index != -1 and currency_index != date_index + 1:
        for i in range(price_index + 1, date_index):
            product_type += parsed_input[i] + ' '
    elif currency_index == price_index and date_index != -1 and currency_index != date_index - 1:
        for i in range(currency_index + 1, date_index):
            product_type += parsed_input[i] + ' '
    elif currency_index == price_index and date_index != -1 and price_index != -1:
        for i in range(price_index + 1, len(parsed_input)):
            product_type += parsed_input[i] + ' '
    else:
        product_type = 'Разное'
    print('end purchase parse')
    return PurchaseInfo(product_date, product_name, product_cost, product_currency, product_type)


def purchase_to_str(purchases: List[PurchaseInfo]):
    str_made = ''
    for i, key in enumerate(purchases):
        str_made += f'{i + 1}. {key.__repr__()}\n'
    return str_made
