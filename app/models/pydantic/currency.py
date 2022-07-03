from pydantic import BaseModel


class Currency(BaseModel):
    description: str
    currency_code: str


class CurrencyRate(BaseModel):
    currency_code: str
    exchange_rate: float


class ConvertCurrency(BaseModel):
    from_currency: str
    to_currency: str
    amount: float


class ConvertedCurrency(BaseModel):
    from_currency: str
    to_currency: str
    provided_amount: float
    converted_amount: float
