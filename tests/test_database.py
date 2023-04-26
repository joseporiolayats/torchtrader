import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from torchtrader.data.ops_specific import Operations
from torchtrader.data.schema import Base

DB_PATH = "test.db"
DB_URI = f"sqlite:///{DB_PATH}"


@pytest.fixture
def test_db():
    # Setup
    test_engine = create_engine(DB_URI)
    Base.metadata.create_all(test_engine)
    test_session = Session(test_engine)

    yield test_session

    # Teardown
    test_session.close()
    os.remove(DB_PATH)


def test_operations(test_db):
    ops = Operations()

    # Create an exchange
    exchange_data = {"name": "Example Exchange"}
    exchange_id = ops.create_exchange(exchange_data)
    assert exchange_id > 0

    # Read exchanges
    exchanges = ops.read_exchange()
    assert len(exchanges) == 1

    # Update an exchange
    exchange_update_data = {"name": "Updated Example Exchange"}
    ops.update_exchange(exchange_data, exchange_update_data)
    updated_exchange = ops.read_exchange(filters=exchange_update_data)
    assert updated_exchange[0].name == "Updated Example Exchange"

    # Create a trading product
    trading_product_data = {
        "name": "Example Trading Product",
        "product_type": "Cryptocurrency",
        "ticker": "EXC",
    }
    trading_product_id = ops.create_trading_product(trading_product_data)
    assert trading_product_id is not None

    # Read trading products
    trading_products = ops.read_trading_product()
    assert len(trading_products) == 1

    # Update a trading product
    trading_product_update_data = {"name": "Updated Example Trading Product"}
    ops.update_trading_product(trading_product_data, trading_product_update_data)
    updated_trading_product = ops.read_trading_product(filters=trading_product_update_data)
    assert updated_trading_product[0].name == "Updated Example Trading Product"

    # Create a trading product exchange relationship
    trading_product_exchange_data = {
        "exchange_id": exchange_id,
        "trading_product_id": trading_product_id,
    }
    trading_product_exchange_id = ops.create_trading_product_exchange(trading_product_exchange_data)
    assert trading_product_exchange_id > 0
    # Read trading product exchange relationships
    trading_product_exchanges = ops.read_trading_product_exchange()
    assert len(trading_product_exchanges) == 1

    # Create an asset
    asset_data = {
        "name": "Example Asset",
        "base_currency": "USD",
        "quote_currency": "EXMP",
        "trading_product_id": trading_product_id,
        "exchange_id": exchange_id,
    }
    asset_id = ops.create_asset(asset_data)
    assert asset_id is not None

    # Read assets
    assets = ops.read_asset()
    assert len(assets) == 1

    # Update an asset
    asset_updates = {"name": "Updated Example Asset"}
    ops.update_asset({"id": asset_id}, asset_updates)
    updated_assets = ops.read_asset(filters=asset_updates)
    assert len(updated_assets) == 1
    assert updated_assets[0].name == "Updated Example Asset"

    # Delete an asset
    ops.delete_asset({"id": asset_id})
    remaining_assets = ops.read_asset()
    assert len(remaining_assets) == 0

    # Delete a trading product exchange relationship
    ops.delete_trading_product_exchange(trading_product_exchange_data)
    remaining_trading_product_exchanges = ops.read_trading_product_exchange()
    assert len(remaining_trading_product_exchanges) == 0

    # Delete a trading product
    ops.delete_trading_product(trading_product_update_data)
    remaining_trading_products = ops.read_trading_product()
    assert len(remaining_trading_products) == 0

    # Delete an exchange
    ops.delete_exchange(exchange_update_data)
    remaining_exchanges = ops.read_exchange()
    assert len(remaining_exchanges) == 0


# Run pytest
if __name__ == "__main__":
    pytest.main(["-v"])
