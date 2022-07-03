from typing import List
from fastapi import APIRouter, Depends
from app.models.pydantic.currency import ConvertCurrency, ConvertedCurrency, Currency
from app.models.pydantic.response import BaseResponse
from app.services import currency
from app.utils.dependencies import has_access
from app.utils.error_handler import OpsException
from app.utils.logger import Logger
from app.utils.response_handler import success


PROTECTED = [Depends(has_access)]


router = APIRouter(prefix="/currencies", tags=["Currencies"], dependencies=PROTECTED)
log = Logger()


@router.get("/", response_model=BaseResponse[List[Currency]])
async def retrieve_currencies():
    try:
        currencies = await currency.get_supported_currencies()
        return success(data=currencies)
    except OpsException as oe:
        log.exception(oe.message, exc_info=oe)
        raise
    except Exception as e:
        log.exception(e)
        raise


@router.post("/convert", response_model=BaseResponse[ConvertedCurrency])
async def convert_currency(request: ConvertCurrency):
    try:
        conversion_rate = await currency.get_currency_rate(
            request.from_currency, request.to_currency
        )
        conversion = await currency.convert_currency(
            conversion_rate.get("exchange_rate"), request.amount
        )
        return success(
            data={
                "from_currency": request.from_currency,
                "to_currency": request.to_currency,
                "provided_amount": request.amount,
                "converted_amount": conversion,
            }
        )
    except OpsException as oe:
        log.exception(oe.message, exc_info=oe)
        raise
    except Exception as e:
        log.exception(e)
        raise
