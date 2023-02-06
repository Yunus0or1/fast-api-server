from pydantic import BaseModel
from typing import Any


class CurrencyRequest(BaseModel):
    init_currency: str
    target_currency: str
    amount: float

    def to_json(self):
        return {
            "init_currency": self.init_currency,
            "target_currency": self.target_currency,
            "amount": self.amount,
        }


class CurrencyResponse(BaseModel):
    target_amount: Any
