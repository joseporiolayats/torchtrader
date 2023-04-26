import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from torchtrader.data.database import GenericDatabase
from torchtrader.data.schema import Base
from torchtrader.data.schema import Exchange
from torchtrader.data.schema import TradingProduct
from torchtrader.data.schema import TradingProductExchange

# import torchtrader.logs

TEST_DB_PATH = "test.db"


# Set up a fixture for test database
@pytest.fixture(scope="module")
def test_database():
    # Create test database
    test_engine = create_engine(f"sqlite:///{TEST_DB_PATH}")
    Base.metadata.create_all(test_engine)
    test_session = Session(test_engine)

    # Set up the test data
    test_exchange = Exchange(name="Test Exchange")
    test_session.add(test_exchange)
    test_session.commit()

    test_product = TradingProduct(name="Test Product", ticker="TEST")
    test_session.add(test_product)
    test_session.commit()

    test_tpe = TradingProductExchange(
        exchange_id=test_exchange.id, trading_product_id=test_product.id
    )
    test_session.add(test_tpe)
    test_session.commit()

    yield test_session

    # Clean up test database
    test_session.close()
    os.remove(TEST_DB_PATH)


def test_create(test_database):
    db = GenericDatabase(TEST_DB_PATH)

    exchange_data = {"name": "New Exchange"}
    exchange_id = db.create(Exchange, exchange_data)
    assert exchange_id > 0

    product_data = {"name": "New Product", "ticker": "NEW"}
    product_id = db.create(TradingProduct, product_data)
    assert product_id > 0

    tpe_data = {"exchange_id": exchange_id, "trading_product_id": product_id}
    tpe_id = db.create(TradingProductExchange, tpe_data)
    assert tpe_id > 0


def test_read(test_database):
    db = GenericDatabase(TEST_DB_PATH)

    exchanges = db.read(Exchange)
    assert len(exchanges) > 0

    trading_products = db.read(TradingProduct)
    assert len(trading_products) > 0

    tpes = db.read(TradingProductExchange)
    assert len(tpes) > 0


def test_update(test_database):
    db = GenericDatabase(TEST_DB_PATH)

    exchange = test_database.query(Exchange).filter_by(name="Test Exchange").first()
    db.update(Exchange, {"id": exchange.id}, {"name": "Updated Exchange"})

    updated_exchange = test_database.query(Exchange).filter_by(id=exchange.id).first()
    assert updated_exchange.name == "Updated Exchange"

    product = test_database.query(TradingProduct).filter_by(name="Test Product").first()
    db.update(TradingProduct, {"id": product.id}, {"name": "Updated Product", "ticker": "UPDT"})

    updated_product = test_database.query(TradingProduct).filter_by(id=product.id).first()
    assert updated_product.name == "Updated Product"
    assert updated_product.ticker == "UPDT"


def test_delete(test_database):
    db = GenericDatabase(TEST_DB_PATH)

    exchange = test_database.query(Exchange).filter_by(name="New Exchange").first()
    db.delete(Exchange, {"id": exchange.id})

    deleted_exchange = test_database.query(Exchange).filter_by(id=exchange.id).first()
    assert deleted_exchange is None

    product = test_database.query(TradingProduct).filter_by(name="New Product").first()
    db.delete(TradingProduct, {"id": product.id})

    deleted_product = test_database.query(TradingProduct).filter_by(id=product.id).first()
    assert deleted_product is None

    tpe = (
        test_database.query(TradingProductExchange)
        .filter_by(trading_product_id=product.id, exchange_id=exchange.id)
        .first()
    )
    if tpe:
        db.delete(TradingProductExchange, {"id": tpe.id})

    deleted_tpe = test_database.query(TradingProductExchange).filter_by(id=tpe.id).first()
    assert deleted_tpe is None


# Run pytest
if __name__ == "__main__":
    pytest.main(["-v"])
