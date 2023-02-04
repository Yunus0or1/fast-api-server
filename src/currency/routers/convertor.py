from typing import Mapping, Any
import requests
from fastapi import APIRouter, Depends
from currency.models.currency_model import CurrencyRequest, CurrencyResponse
from currency.middlewares.jwt_token_middleware import verify_token
from currency.util.log import log
from fastapi import Depends

router = APIRouter(
    tags=["convertor"],
    responses={404: {"description": "No currency data found, sorry!"}},
)


@router.get("/", dependencies=[Depends(verify_token)])
async def root() -> Mapping[str, str]:
    log.info('Hello 22222')
    return {"message": "Welcome to the Currency Convertor API"}


@router.post("/convert", response_model=CurrencyResponse)
async def convert(
        currency_request: CurrencyRequest
) -> CurrencyResponse:
    amount = None
    while True:
        try:
            amount = currency_request.amount
        except:
            print('The amount must be a numeric value!')
            continue

        if not amount > 0:
            print('The amount must be greater than 0')
            continue
        else:
            break

    url = ('https://api.apilayer.com/fixer/convert?to='+ currency_request.target_currency + '&from=' + currency_request.init_currency +'&amount=' + str(amount))

    payload = {}
    headers = {'apikey': 'YOUR-API-KEY'}
    response = requests.request('GET', url, headers=headers, data=payload)
    status_code = response.status_code

    if status_code != 200:
        print('Uh oh, there was a problem. Please try again later')
        raise Exception("Something went wrong")

    result = response.json()
    return CurrencyResponse(target_amount=result['result'])
