# simplex_interview
Create an API to get a quote for exchange rate between USD, ILS and EUR

## Setup (once)
```
docker-compose build
```

## Run
```
docker-compose up
```

## Test
### API request for quote for USD to EUR exchange rate
Request:
```
curl http://127.0.0.1:5000/api/quote?from_currency_code=USD&to_currency_code=EUR&amount=100

```
Response:
```
{
  "amount": 86.1,
  "currency_code": "EUR",
  "exchange_rate": 0.861,
  "provider_name": "Exchange Rate API"
}
```
