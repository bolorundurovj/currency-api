from typing import List
import httpx
from app.models.pydantic.currency import Currency, CurrencyRate
from app.utils.error_handler import OpsException
from app.utils.logger import Logger

BASE_URL = "https://api.exchangerate.host/"


client = httpx.AsyncClient()
log = Logger()


async def get_supported_currencies() -> List[Currency]:
    """Retrieves and maps supported currencies from external api

    Raises:
        OpsException: _description_

    Returns:
        List[Currency]: An array of currency codes and descriptions
    """
    try:
        response = await client.get(f"{BASE_URL}/symbols")
        jsonified_response = response.json()
        return [
            {
                "currency_code": currency.get("code"),
                "description": currency.get("description"),
            }
            for currency in list(jsonified_response["symbols"].values())
        ]
    except Exception:
        raise OpsException()


async def get_currency_rate(from_currency: str, to_currency) -> CurrencyRate:
    """Retrieves currency conversion rate from external api and maps response

    Args:
        from_currency (str): base currency
        to_currency (_type_): output currency

    Raises:
        OpsException: Operation Exception

    Returns:
        CurrencyRate: the currency conversion rate
    """
    params = {"symbols": to_currency, "base": from_currency}
    try:
        response = await client.get(f"{BASE_URL}/latest", params=params)
        jsonified_response = response.json()
        return {
            "currency_code": list(jsonified_response["rates"].keys())[0],
            "exchange_rate": list(jsonified_response["rates"].values())[0],
        }
    except Exception:
        raise OpsException()


async def convert_currency(conversion_rate: float, amount: float) -> float:
    """Carries out currency conversion calculation

    Args:
        conversion_rate (float): the conversion rate in decimal form
        amount (float): the amount to be converted

    Returns:
        float: converted amount
    """
    return conversion_rate * amount
