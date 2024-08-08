from fastapi import APIRouter, Path, status
from fastapi.responses import JSONResponse

router = APIRouter(tags=["Stock"])


@router.get(
    path="/stock/{stock_symbol}",
    response_class=JSONResponse,
    name="stock",
    status_code=status.HTTP_200_OK,
)
async def check_health(
    *, stock_symbol: str = Path(description="Stock Symbol")
) -> JSONResponse:
    return JSONResponse(content={"stock_symbol": stock_symbol})
