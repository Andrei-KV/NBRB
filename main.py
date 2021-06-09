import requests
import sys
import os


class MyError(Exception):
    pass


def creat_currency_cache():
    res_cache = requests.get('https://www.nbrb.by/api/exrates/currencies')
    currency_control_list = [item["Cur_Abbreviation"] for item in res_cache.json()]
    with open('currency.cache', 'w') as f:
        [f.writelines(item + '\n') for item in currency_control_list]


def input_currency_name():
    try:
        input_name = sys.argv[1].upper()
    except IndexError:
        while True:
            input_name = input('Currency name (ISO 4217):').upper()
            if input_name and control_match_iso(input_name):
                break
            print('No name base matches. Try again.')
    return input_name


def control_match_iso(control_name):
    with open('currency.cache', 'r') as f:
        cache = [var.strip() for var in f.readlines()]
    if control_name in cache:
        return True
    else:
        return False


def fetch_data(url):
    res = requests.get(url)
    try:
        if res.status_code != 200:
            raise MyError
    except MyError:
        return 'Response error. Try after vacations.'
    else:
        return print_requests(res)


def print_requests(res):
    res = res.json()
    return f'{res["Cur_OfficialRate"]} {res["Date"].split("T")[0]} {res["Date"].split("T")[1]}'


# Create currency cache if not in directory
if 'currency.cache' not in os.listdir(path='.'):
    creat_currency_cache()

currency_name = input_currency_name()
res = requests.get(f'https://www.nbrb.by/api/exrates/rates/{currency_name}?parammode=2').json()
url = f'https://www.nbrb.by/api/exrates/rates/{currency_name}?parammode=2'
print(fetch_data(url))
