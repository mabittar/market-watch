from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid_extensions import uuid7

from . import Base


class Stock(Base):
    __tablename__ = "stock"

    id = Column(String, nullable=False, primary_key=True)
    company_code = Column(String, nullable=False)
    company_name = Column(String, nullable=True)
    request_data = Column(String, nullable=False)

    stock_values = relationship("StockTimeSeries", back_populates="stock")
    performance_data = relationship(
        "StockPerformance", uselist=False, back_populates="stock"
    )
    market_cap = relationship("MarketCap", uselist=False, back_populates="stock")


class StockTimeSeries(Base):
    __tablename__ = "stock_timeseries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    stock_id = Column(String, ForeignKey("stock.id"), nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    date = Column(String, nullable=False)

    stock = relationship("Stock", back_populates="stock_values")


class MarketCap(Base):
    __tablename__ = "market_cap"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    stock_id = Column(String, ForeignKey("stock.id"), nullable=False)
    currency = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    date = Column(String, nullable=False)

    stock = relationship("Stock", back_populates="market_cap")


class StockPerformance(Base):
    __tablename__ = "stock_performance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    stock_id = Column(String, ForeignKey("stock.id"), nullable=False)
    five_days = Column(Float, nullable=False)
    one_month = Column(Float, nullable=False)
    three_months = Column(Float, nullable=False)
    year_to_date = Column(Float, nullable=False)
    one_year = Column(Float, nullable=False)
    date = Column(String, nullable=False)

    stock = relationship("Stock", back_populates="performance_data")


class StockOperation(Base):
    __tablename__ = "stock_operation"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    stock_id = Column(String, ForeignKey("stock.id"), nullable=False)
    operation_date = Column(String, nullable=False)
    purchased_amount = Column(Float, nullable=False)
    purchased_status = Column(String, nullable=False)


class Competitor(Base):
    __tablename__ = "competitor"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_id = Column(String, ForeignKey("stock.id"), nullable=False)
    name = Column(String, nullable=False)
