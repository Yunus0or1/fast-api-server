from typing import Mapping, Any
import requests
from fastapi import APIRouter, Depends, HTTPException
from currency.models.currency_model import CurrencyRequest, CurrencyResponse
from currency.middlewares.jwt_token_middleware import verify_token
from currency.util.log import log
from fastapi import Depends
from currency import config
from fastapi.responses import JSONResponse

router = APIRouter(
    tags=["convertor"],
    responses={404: {"description": "No currency data found, sorry!"}},
)


@router.get("/", dependencies=[Depends(verify_token)])
async def root() -> Mapping[str, str]:
    try:
        return {"message": "Welcome to the Currency Convertor API"}
    except Exception as error:
        log.error('Error in root => ', error)
        raise HTTPException(500, detail="Something went wrong.")


@router.post("/convert", response_model=CurrencyResponse)
async def convert(
        currency_request: CurrencyRequest
) -> Any:
    try:
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

        url = (config.CONVERTER_API + '?to=' + currency_request.target_currency +
               '&from=' + currency_request.init_currency + '&amount=' + str(amount))

        payload = {}
        headers = {'apikey': config.CONVERTER_API_KEY}
        response = requests.request('GET', url, headers=headers, data=payload)

        result = response.json()
        status_code = response.status_code

        if status_code != 200 or "error" in result:
            errorMessage = result["error"]["info"]
            log.error('Error in convert status_code =>', result)
            return JSONResponse(status_code=status_code, content={"error": "Something went wrong in fetching API. Error => " + errorMessage})

        result = response.json()
        return CurrencyResponse(target_amount=result['result'])

    except Exception as error:
        log.error('Error in convert =>')
        raise HTTPException(500, message="Something went wrong.")
