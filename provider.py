from collections import namedtuple
import logging


class Provider(namedtuple('Provider', ['name', 'url'])):
    def get_exchange_rate(self, from_currency_code, to_currency_code):
        import requests
        api_url = f'{self.url}{from_currency_code}'
        currency_pair = f'{from_currency_code}{to_currency_code}'
        try:
            response = requests.get(api_url).json()
            exchange_rate = response.get('rates').get(to_currency_code)
            if exchange_rate is not None:
                logging.info(f'{self.name}: {currency_pair} rate: {exchange_rate}')
            else:
                logging.warn(f'{self.name}: No rate for {currency_pair}')
            return exchange_rate
        except Exception as e:
            logging.error(f'{self.name}: exception while getting quote for currency pair {currency_pair}: {e}')
            return None
