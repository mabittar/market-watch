from fastapi import APIRouter, Path, status
from fastapi.responses import JSONResponse

from ..models.schema.stock import Stock

router = APIRouter(tags=["Stock"])


@router.get(
    path="/stock/{stock_symbol}",
    response_class=JSONResponse,
    name="stock",
    status_code=status.HTTP_200_OK,
)
async def check_health(
    *, stock_symbol: str = Path(description="Stock Symbol")
) -> Stock:
    return Stock(stock_symbol=stock_symbol)
