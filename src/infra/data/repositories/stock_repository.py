
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid_extensions import uuid7

from src.models.schema.stock import (
    CompetitorSchema,
    StockMarketCapSchema,
    StockPerformanceSchema,
    StockValuesSchema,
)

from ..entities import (
    Competitor,
    MarketCap,
    Stock,
    StockOperation,
    StockPerformance,
    StockTimeSeries,
)


class StockRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_stock(
        self, company_code: str, company_name: str | None, request_data: str, **kwargs
    ) -> Stock:
        result = await self.db.execute(
            select(Stock).where(Stock.company_code == company_code)
        )
        existing_stock = result.scalars().first()

        if existing_stock:
            return existing_stock

        id = str(uuid7())
        stock = Stock(
            id=id,
            company_code=company_code,
            company_name=company_name,
            request_data=request_data,
        )
        self.db.add(stock)
        await self.db.commit()
        await self.db.refresh(stock)
        return stock

    async def get_stock_by_company_code(self, company_code: str) -> Stock | None:
        stock = (
            await self.db.scalars(
                select(Stock).where(Stock.company_code == company_code)
            )
        ).first()

        if not stock:
            raise HTTPException(
                status_code=404, detail=f"stock not found for symbol: {company_code}"
            )

        return stock

    async def add_stock_timeseries(
        self,
        stock_id: str,
        open: float,
        high: float,
        low: float,
        close: float,
        date_str: str,
    ) -> None:
        query = select(StockTimeSeries).where(
            StockTimeSeries.stock_id == stock_id, StockTimeSeries.date == date_str
        )
        result = await self.db.execute(query)
        existing_timeseries = result.scalars().first()

        if existing_timeseries:
            return None

        timeseries = StockTimeSeries(
            id=uuid7(),
            stock_id=stock_id,
            open=open,
            high=high,
            low=low,
            close=close,
            date=date_str,
        )
        self.db.add(timeseries)
        await self.db.commit()

    async def get_stock_timeseries(self, stock_id: str) -> list[StockValuesSchema]:

        ts = (
            await self.db.scalars(
                select(StockTimeSeries).where(StockTimeSeries.stock_id == stock_id)
            )
        ).all()
        return [
            StockValuesSchema(
                open=t.open,  # type: ignore
                close=t.close,  # type: ignore
                high=t.high,  # type: ignore
                low=t.low,  # type: ignore
                date=t.date,  # type: ignore
            )
            for t in ts
        ]

    async def add_market_cap(
        self, stock_id: str, currency: str, value: float, date_str: str
    ) -> None:
        query = select(MarketCap).where(
            MarketCap.stock_id == stock_id, MarketCap.date == date_str
        )
        result = await self.db.execute(query)
        existing_market_cap = result.scalars().first()

        if existing_market_cap:
            return None

        market_cap = MarketCap(
            id=uuid7(), stock_id=stock_id, currency=currency, value=value, date=date_str
        )
        self.db.add(market_cap)
        await self.db.commit()

    async def get_market_cap(self, stock_id: str) -> StockMarketCapSchema:
        mtk_cap = (
            await self.db.scalars(
                select(MarketCap)
                .where(MarketCap.stock_id == stock_id)
                .order_by(MarketCap.id.desc())
            )
        ).first()
        return StockMarketCapSchema(
            currency=mtk_cap.currency,  # type: ignore
            value=mtk_cap.value,  # type: ignore
        )

    async def add_stock_performance(
        self,
        stock_id: str,
        five_days: float,
        one_month: float,
        three_months: float,
        year_to_date: float,
        one_year: float,
        date_str: str,
    ) -> None:

        query = select(StockPerformance).where(
            StockPerformance.stock_id == stock_id, StockPerformance.date == date_str
        )
        result = await self.db.execute(query)
        existing_performance = result.scalars().first()

        if existing_performance:
            return None

        performance = StockPerformance(
            id=uuid7(),
            stock_id=stock_id,
            five_days=five_days,
            one_month=one_month,
            three_months=three_months,
            year_to_date=year_to_date,
            one_year=one_year,
            date=date_str,
        )
        self.db.add(performance)
        await self.db.commit()

    async def get_stock_performance(
        self, stock_id: str, date_str: str
    ) -> StockPerformanceSchema:
        performance = (
            await self.db.scalars(
                select(StockPerformance).where(
                    StockPerformance.stock_id == stock_id,
                    StockPerformance.date == date_str,
                )
            )
        ).first()
        return StockPerformanceSchema(
            five_days=performance.five_days,  # type: ignore
            one_month=performance.one_month,  # type: ignore
            three_months=performance.three_months,  # type: ignore
            year_to_date=performance.year_to_date,  # type: ignore
            one_year=performance.one_year,  # type: ignore
        )

    async def add_stock_operation(
        self,
        stock_id: str,
        request_data: str,
        purchased_amount: float,
        purchased_status: str,
        **kwargs,
    ) -> None:
        operation = StockOperation(
            id=uuid7(),
            stock_id=stock_id,
            operation_date=request_data,
            purchased_amount=purchased_amount,
            purchased_status=purchased_status,
        )
        self.db.add(operation)
        await self.db.commit()

    async def get_stock_operations(self, stock_id: str) -> list[StockOperation]:
        operations = (
            await self.db.scalars(
                select(StockOperation).where(StockOperation.stock_id == stock_id)
            )
        ).all()
        return [
            StockOperation(
                stock_id=operation.stock_id,
                purchased_amount=operation.purchased_amount,
                operation_date=operation.operation_date,
                purchased_status=operation.purchased_status,
            )
            for operation in operations
        ]

    async def get_stock_operation_by_date(
        self, stock_id: str, operation_date: str
    ) -> StockOperation | None:
        operation = (
            await self.db.scalars(
                select(StockOperation).where(
                    StockOperation.stock_id == stock_id,
                    StockOperation.operation_date == operation_date,
                )
            )
        ).first()
        if operation is None:
            return None
        return StockOperation(
            stock_id=operation.stock_id,
            purchased_amount=operation.purchased_amount,
            operation_date=operation.operation_date,
            purchased_status=operation.purchased_status,
        )

    async def add_competitor(self, stock_id: str, name: str) -> None:
        query = select(Competitor).where(
            Competitor.stock_id == stock_id, Competitor.name == name
        )
        result = await self.db.execute(query)
        existing_competitor = result.scalars().first()

        if existing_competitor:
            return None
        competitor = Competitor(stock_id=stock_id, name=name)
        self.db.add(competitor)
        await self.db.commit()

    async def get_competitors(self, stock_id: str) -> list[CompetitorSchema]:
        competitors = (
            await self.db.scalars(
                select(Competitor).where(Competitor.stock_id == stock_id)
            )
        ).all()

        return [
            CompetitorSchema(name=str(competitor.name)) for competitor in competitors
        ]
