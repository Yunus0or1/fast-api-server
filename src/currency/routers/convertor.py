from typing import Mapping, Any
import requests
from fastapi import APIRouter, Depends, HTTPException
from currency.models.currency_model import CurrencyRequest, CurrencyResponse
from currency.middlewares.jwt_token_middleware import verify_token
from currency.util.log import log
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


@router.post("/convert", dependencies=[Depends(verify_token)], response_model=CurrencyResponse)
async def convert(
        currency_request: CurrencyRequest
) -> Any:
    try:
        amount = currency_request.amount
        if amount is None:
            return JSONResponse(status_code=400,
                                content={"message": "The amount must be a numeric value!",
                                         "error": True})

        if not amount > 0:
            return JSONResponse(status_code=400,
                                content={"message": "The amount must be greater than 0.",
                                         "error": True})

        if amount > 999999999999999:
            return JSONResponse(status_code=400,
                                content={"message": "The amount is too big.",
                                         "error": True})

        result = fetchCurrencyApiData(currency_request)

        if "error" in result:
            return JSONResponse(status_code=400,
                                content={"message": result["message"], "error": True})

        return CurrencyResponse(target_amount=result['message'])

    except Exception as error:
        log.error('Error in convert => ', error)
        raise HTTPException(500, message="Something went wrong.")


def fetchCurrencyApiData(currency_request: CurrencyRequest) -> Any:
    url = (config.CONVERTER_API + '?to=' + currency_request.target_currency +
           '&from=' + currency_request.init_currency + '&amount=' + str(currency_request.amount))
    payload = {}
    headers = {'apikey': config.CONVERTER_API_KEY}

    retry = 0
    while retry < 2:
        try:
            response = requests.request(
                'GET', url, headers=headers, data=payload)
            result = response.json()
            status_code = response.status_code

            if status_code != 200 or "error" in result:
                errorMessage = result["error"]["info"]
                log.error('Error in convert status_code =>', result)
                return {"error": True, "message": errorMessage, "status_code": status_code}

            return {"message": result['result'], "status_code": status_code}
        except Exception as error:
            log.error('Error in fetchCurrencyApiData =>', error)
            retry = retry + 1

    return {"error": True, "message": "Could not fetch from currency", "status_code": 500}
