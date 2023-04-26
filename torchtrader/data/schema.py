"""
torchtrader/data/schema.py
"""
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    trading_product_id = None
    exchange_id = None
    name = None
    _decl_class_registry = None
    date_time = None
    id: int


class Exchange(Base):
    __tablename__ = "exchanges"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    trading_product_exchanges = relationship(
        "TradingProductExchange", back_populates="exchange", cascade="all, delete-orphan"
    )


class TradingProduct(Base):
    __tablename__ = "trading_products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    product_type: Mapped[str] = mapped_column(String(50), nullable=False)
    ticker: Mapped[str] = mapped_column(String(20), nullable=False)
    trading_product_exchanges = relationship(
        "TradingProductExchange", back_populates="trading_product", cascade="all, delete-orphan"
    )


class TradingProductExchange(Base):
    __tablename__ = "trading_product_exchanges"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exchange_id: Mapped[int] = mapped_column(Integer, ForeignKey("exchanges.id"), nullable=False)
    trading_product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("trading_products.id"), nullable=False
    )
    trading_product = relationship("TradingProduct", back_populates="trading_product_exchanges")
    exchange = relationship("Exchange", back_populates="trading_product_exchanges")


class Asset(Base):
    __tablename__ = "assets"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    base_currency: Mapped[str] = mapped_column(String(20), nullable=False)
    quote_currency: Mapped[str] = mapped_column(String(20), nullable=False)
    trading_product_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("trading_products.id"), nullable=False
    )
    exchange_id: Mapped[int] = mapped_column(Integer(), ForeignKey("exchanges.id"), nullable=False)
    trading_product = relationship("TradingProduct", backref="assets")
    exchange = relationship("Exchange", backref="assets")
    data_points = relationship("DataPoint", back_populates="asset")


class DataPoint(Base):
    __tablename__ = "data_points"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    asset_id: Mapped[int] = mapped_column(Integer(), ForeignKey("assets.id"), nullable=False)
    date_time: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    open: Mapped[float] = mapped_column(Float(), nullable=False)
    high: Mapped[float] = mapped_column(Float(), nullable=False)
    low: Mapped[float] = mapped_column(Float(), nullable=False)
    close: Mapped[float] = mapped_column(Float(), nullable=False)
    volume: Mapped[float] = mapped_column(Float(), nullable=False)
    asset = relationship("Asset", back_populates="data_points")
