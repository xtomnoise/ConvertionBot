import requests
import json
import math
from configs import APIKEY, keys

class ConvException(Exception):
    ...

class ConvertValute:
    @staticmethod
    def get_price(base, quote, amount):

        try:
            amount = float(amount)
        except ValueError:
            raise ConvException(f'Неправильный параметр количества {amount}.')

        try:
            base_simb = keys[base]
        except KeyError:
            raise ConvException(f'Неизвестная валюта {base}.')

        try:
            quote_simb = keys[quote]
        except KeyError:
            raise ConvException(f'Неизвестная валюта {quote}.')

        if base == quote:
            raise ConvException(f'Невозможно перевести {quote} в {quote}.')

        pair = ''.join((base_simb, quote_simb))

        r = requests.get(f'https://currate.ru/api//?get=rates&pairs={pair}&key={APIKEY}')
        rates = json.loads(r.content)

        return round(float(rates['data'][pair])*amount, 2)