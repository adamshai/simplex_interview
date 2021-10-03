from flask import Flask, request
from provider import Provider
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


CURRENCY_CODES = ['USD', 'EUR', 'ILS']
EXCHANGE_PROVIDERS = [
    Provider('Exchange Rate API', 'https://open.er-api.com/v6/latest/'),
    Provider('Frankfurter', 'https://api.frankfurter.app/latest?from='),
]


def get_exchange_rates(from_currency_code, to_currency_code):
    rates = [(p.get_exchange_rate(from_currency_code, to_currency_code), p) for p in EXCHANGE_PROVIDERS]
    return rates


def get_min_exchange_rate(from_currency_code, to_currency_code):
    import math
    import random

    rates = get_exchange_rates(from_currency_code, to_currency_code)
    min_rate = math.inf
    providers = []
    for rate, provider in rates:
        if rate is None:
            continue
        if rate < min_rate:
            min_rate = rate
            providers = [provider]
        elif rate == min_rate:
            providers.append(provider)
    if len(providers) == 0:
        exchange_rate = None
        provider_name = None
    elif len(providers) == 1:
        exchange_rate = min_rate
        provider_name = providers[0].name
    else:
        exchange_rate = min_rate
        provider_name = random.choice(providers).name
    return exchange_rate, provider_name


@app.route('/api/quote')
def get_quote():
    import timeit

    start = timeit.default_timer()
    logging.info(f'get_quote({request.args})')
    response = {}
    try:
        from_currency_code = request.args.get('from_currency_code')
        amount = int(request.args.get('amount'))
        to_currency_code = request.args.get('to_currency_code')

        exchange_rate, provider = get_min_exchange_rate(from_currency_code, to_currency_code)
        if exchange_rate is not None:
            response = {
                'exchange_rate': exchange_rate,
                'currency_code': to_currency_code,
                'amount': amount * exchange_rate,
                'provider_name': provider
            }
    except Exception as e:
        logging.error(f'Caught exception: {e}')

    stop = timeit.default_timer()
    logging.info(f'get_quote() completed in {stop - start} seconds')
    logging.debug(f'response={response}')
    return response
