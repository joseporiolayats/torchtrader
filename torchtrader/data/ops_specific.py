"""
torchtrader/data/ops_specific.py
"""
from typing import Any
from typing import Dict
from typing import Type

from torchtrader.data.database import GenericDatabase
from torchtrader.data.schema import Asset
from torchtrader.data.schema import Base
from torchtrader.data.schema import Exchange
from torchtrader.data.schema import TradingProduct
from torchtrader.data.schema import TradingProductExchange


class OpsSpecific(GenericDatabase):
    def __init__(self):
        super().__init__()

    def create_exchange(self, data: Dict[str, Any]) -> int | None:
        return self.create(Exchange, data)

    def read_exchange(self, filters: Dict[str, Any] = None) -> list[Type[Base]]:
        return self.read(Exchange, filters)

    def update_exchange(self, record: Dict[str, Any], updates: Dict[str, Any]) -> None:
        self.update(Exchange, record, updates)

    def delete_exchange(self, data: Dict[str, Any]) -> None:
        self.delete(Exchange, data)

    def create_trading_product(self, data: Dict[str, Any]) -> int:
        return self.create(TradingProduct, data)

    def read_trading_product(self, filters: Dict[str, Any] = None) -> list[Type[Base]]:
        return self.read(TradingProduct, filters)

    def update_trading_product(self, record: Dict[str, Any], updates: Dict[str, Any]) -> None:
        self.update(TradingProduct, record, updates)

    def delete_trading_product(self, data: Dict[str, Any]) -> None:
        self.delete(TradingProduct, data)

    def create_asset(self, data: Dict[str, Any]) -> int:
        return self.create(Asset, data)

    def read_asset(self, filters: Dict[str, Any] = None) -> list[Type[Base]]:
        return self.read(Asset, filters)

    def update_asset(self, record: Dict[str, Any], updates: Dict[str, Any]) -> None:
        self.update(Asset, record, updates)

    def delete_asset(self, data: Dict[str, Any]) -> None:
        self.delete(Asset, data)

    def create_trading_product_exchange(self, data: Dict[str, Any]) -> int:
        return self.create(TradingProductExchange, data)

    def read_trading_product_exchange(self, filters: Dict[str, Any] = None) -> list[Type[Base]]:
        return self.read(TradingProductExchange, filters)

    def update_trading_product_exchange(
        self, record: Dict[str, Any], updates: Dict[str, Any]
    ) -> None:
        self.update(TradingProductExchange, record, updates)

    def delete_trading_product_exchange(self, data: Dict[str, Any]) -> None:
        self.delete(TradingProductExchange, data)
