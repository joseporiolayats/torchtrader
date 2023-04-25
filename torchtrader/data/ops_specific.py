"""
torchtrader/data/ops_specific.py
"""
from typing import Any
from typing import Dict
from typing import Type

from torchtrader.data.database import TorchtraderDatabase
from torchtrader.data.schema import Asset
from torchtrader.data.schema import Base
from torchtrader.data.schema import Exchange
from torchtrader.data.schema import TradingProduct
from torchtrader.data.schema import TradingProductExchange


class OpsSpecific(TorchtraderDatabase):
    def __init__(self):
        super().__init__()

    # Exchange operations
    def create_exchange(self, data: Dict[str, Any]) -> int | None:
        return self.create_table(Exchange, data)

    def read_exchange(self, filters: Dict[str, Any] = None) -> list[Type[Base]]:
        return self.read_table(Exchange, filters)

    def update_exchange(self, record: Dict[str, Any], updates: Dict[str, Any]) -> None:
        self.update_table(Exchange, record, updates)

    def delete_exchange(self, data: Dict[str, Any]) -> None:
        self.delete_table(Exchange, data)

    # Trading product operations
    def create_trading_product(self, data: Dict[str, Any]) -> int:
        return self.create_table(TradingProduct, data)

    def read_trading_product(self, filters: Dict[str, Any] = None) -> list[Type[Base]]:
        return self.read_table(TradingProduct, filters)

    def update_trading_product(self, record: Dict[str, Any], updates: Dict[str, Any]) -> None:
        self.update_table(TradingProduct, record, updates)

    def delete_trading_product(self, data: Dict[str, Any]) -> None:
        self.delete_table(TradingProduct, data)

    # Asset operations
    def create_asset(self, data: Dict[str, Any]) -> int:
        return self.create_table(Asset, data)

    def read_asset(self, filters: Dict[str, Any] = None) -> list[Type[Base]]:
        return self.read_table(Asset, filters)

    def update_asset(self, record: Dict[str, Any], updates: Dict[str, Any]) -> None:
        self.update_table(Asset, record, updates)

    def delete_asset(self, data: Dict[str, Any]) -> None:
        self.delete_table(Asset, data)

    # Trading product exchange relationship operations
    def create_trading_product_exchange(self, data: Dict[str, Any]) -> int:
        return self.create_table(TradingProductExchange, data)

    def read_trading_product_exchange(self, filters: Dict[str, Any] = None) -> list[Type[Base]]:
        return self.read_table(TradingProductExchange, filters)

    def update_trading_product_exchange(
        self, record: Dict[str, Any], updates: Dict[str, Any]
    ) -> None:
        self.update_table(TradingProductExchange, record, updates)

    def delete_trading_product_exchange(self, data: Dict[str, Any]) -> None:
        self.delete_table(TradingProductExchange, data)
