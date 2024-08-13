from datetime import datetime

from fastapi import APIRouter, HTTPException, Path, status
from fastapi.responses import JSONResponse

from ..application.create_stock_operation_application import CreateStockOperation
from ..application.stock_application import GetStockOperationApplication
from ..infra.db.session import DBSessionDep
from ..models.schema.stock import (
    StockOperationReponse,
    StockOperationRequest,
    StockResponse,
)

router = APIRouter(tags=["Stock"])

min_stock_length = 2


@router.get(
    path="/stock/{stock_symbol}/{date}",
    response_class=JSONResponse,
    name="get stock",
    status_code=status.HTTP_200_OK,
)
async def get_stock(
    *,
    stock_symbol: str = Path(description="Stock Symbol"),
    date: str = Path(description="Stock operation Date - format YYYY-MM-DD"),
    db_session: DBSessionDep,
) -> StockResponse:
    if stock_symbol.__len__() < min_stock_length:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="stock_symbol must be greater than 2 letters",
        )
    try:
        _str = datetime.strptime(date, "%Y-%m-%d").date()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid date - format YYYY-MM-DD",
        )

    return await GetStockOperationApplication().execute(stock_symbol, date, db_session)


@router.post(
    path="/stock/{stock_symbol}",
    response_class=JSONResponse,
    name="create stock operations",
    status_code=status.HTTP_201_CREATED,
)
async def create_stock_operation(
    *,
    stock_symbol: str = Path(description="Stock Symbol"),
    operation: StockOperationRequest,
    db_session: DBSessionDep,
) -> StockOperationReponse:
    if stock_symbol.__len__() < min_stock_length:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="stock_symbol must be greater than 2 letters",
        )
    if operation.date is not None:
        try:
            _date = datetime.strptime(operation.date, "%Y-%m-%d").date()
            if _date >= datetime.now().date():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="invalid date must be less than today",
                )

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="invalid date format, must be YYYY-MM-DD",
            )
    return await CreateStockOperation().execute(
        stock_symbol=stock_symbol, operation=operation, db_session=db_session
    )
