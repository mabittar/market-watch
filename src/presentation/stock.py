from fastapi import APIRouter, HTTPException, Path, status
from fastapi.responses import JSONResponse

from ..application.create_stock_operation_application import CreateStockOperation
from ..application.stock_application import StockApplication
from ..models.schema.stock import StockOperation, StockOperationReponse, StockResponse

router = APIRouter(tags=["Stock"])

min_stock_length = 2


@router.get(
    path="/stock/{stock_symbol}",
    response_class=JSONResponse,
    name="get stock",
    status_code=status.HTTP_200_OK,
)
async def get_stock(
    *, stock_symbol: str = Path(description="Stock Symbol")
) -> StockResponse:
    if stock_symbol.__len__() < min_stock_length:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="stock_symbol must be greater than 2 letters",
        )
    return await StockApplication().execute(stock_symbol)


@router.post(
    path="/stock/{stock_symbol}",
    response_class=JSONResponse,
    name="create stock operations",
    status_code=status.HTTP_201_CREATED,
)
async def create_stock_operation(
    *, stock_symbol: str = Path(description="Stock Symbol"), operation: StockOperation
) -> StockOperationReponse:
    if stock_symbol.__len__() < min_stock_length:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="stock_symbol must be greater than 2 letters",
        )
    return await CreateStockOperation().execute(
        stock_symbol=stock_symbol, amount=operation.amount
    )
