# Currency Convertor
This is an API to convert currencies.

## Objectives
* To improve this service however you see fit.
* This should be timeboxed to around 1-2 hours.
* Poetry is not a hard requirement, pip or conda would suffice.
* Example request body
```json
{
  "init_currency": "GBP",
  "target_currency": "EUR",
  "amount": 10.0
}
```

## Installation & Setup

Minimum requirements
* Could not use Poetry for different version problem. Moved to pip
* install using this command => pip install -r requirements.txt
* Pushed the .env file for the convenience. Just paste the API key. You can get the API from here => https://apilayer.com/marketplace/fixer-api

## Run

* Change directory to => src
* Run this command => python -m currency

## Test

* Be in the root directory.
* python -m pytest -s

## Doc
* The postman collections can be used to test the APIs.
* The docs can be accessed through `http://localhost:9898/docs`