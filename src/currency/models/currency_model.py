from pydantic import BaseModel
from typing import Any


class CurrencyRequest(BaseModel):
    init_currency: str
    target_currency: str
    amount: float


class CurrencyResponse(BaseModel):
    target_amount: Any
