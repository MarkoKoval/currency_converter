import requests
from datetime import datetime
import json

api_source = "https://bank.gov.ua/NBUStatService/v1" \
             "/statdirectory/exchange?date={}&json"


def get_currency_rates():
    """extract currency rates for current day using API"""

    r = requests.get(api_source.format(
        "".join(str(datetime.now()).split()[0].split('-'))))
    return {item["cc"]: (item["txt"], item["rate"]) for item
            in json.loads(r.text)}


class Ccy:
    """Currency convertor class"""

    # extract currency rates from API
    currency_rates = get_currency_rates()

    def __init__(self, amount, currency):

        if not isinstance(currency, str) or \
                (currency not in self.currency_rates and currency != "UAH")\
                or not isinstance(amount, float) or amount < 0:
            raise Exception("Enter correct data")

        self._amount = amount
        self._currency = currency

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, count):
        if not isinstance(count, float) or count < 0:
            raise Exception("Enter correct data")
        self._amount = count

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, name):
        if not isinstance(name, str) or \
                (name not in self.currency_rates and name != "UAH"):
            raise Exception("Enter correct data")
        self._currency = name

    def __str__(self):
        return " {} {}".format(self.amount, self.currency)

    def get_rate(self, base_currency, secondary_currency):
        """ get rate base currency to secondary"""
        if base_currency == "UAH":
            return self.currency_rates[secondary_currency][1]
        elif secondary_currency == "UAH":
            return 1.0 / self.currency_rates[base_currency][1]
        else:
            return self.currency_rates[secondary_currency][1]\
                   / self.currency_rates[base_currency][1]

    def find_rate(self, amount, base_currency, secondary_currency):
        return amount * self.get_rate(base_currency, secondary_currency)

    def __add__(self, secondary):
        """ add converted secondary currency to base"""
        if self.currency == secondary.currency:
            return Ccy(self.amount + secondary.amount, self.currency)
        elif self.currency != secondary.currency and (
                (self.currency in self.currency_rates
                 and secondary.currency in self.currency_rates) or
                (self.currency == "UAH" and
                 secondary.currency in self.currency_rates) or
                (self.currency in self.currency_rates
                 and secondary.currency == "UAH")):
            return Ccy(self.amount + self.find_rate(
                secondary.amount, self.currency,
                secondary.currency), self.currency)
        else:
            raise Exception("Enter correct data")

    def __sub__(self, secondary):
        """ subtract converted secondary currency from base"""
        if self.currency == secondary.currency \
                and self.amount > secondary.amount:
            return Ccy(self.amount - secondary.amount, self.currency)
        elif self.currency != secondary.currency and (
                (self.currency in self.currency_rates and
                 secondary.currency in self.currency_rates) or
                (self.currency == "UAH" and
                 secondary.currency in self.currency_rates) or
                (self.currency in self.currency_rates
                 and secondary.currency == "UAH")):
            converted = self.find_rate(secondary.amount,
                                       self.currency, secondary.currency)

            if converted > self.amount:
                Exception("Enter correct data")
            return Ccy(self.amount - converted, self.currency)
        else:
            raise Exception("Enter correct data")
