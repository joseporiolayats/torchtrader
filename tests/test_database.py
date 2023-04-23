from datetime import datetime

import pytest

from torchtrader.data.database import ExchangeBase
from torchtrader.data.database import TorchtraderDatabase


@pytest.fixture(scope="module")
def database():
    db = TorchtraderDatabase()
    db.connect_database()
    yield db
    db.close_session()


@pytest.fixture(scope="module")
def table(database):
    table_class = database.create_table("test_binance", "1h", is_crypto=True)
    ExchangeBase.metadata.create_all(database.db_engine)
    yield table_class
    table_class.__table__.drop(database.db_engine)


def test_create_table(database):
    """
    Test creating a table class for a specified exchange and timeframe.
    """
    table_class = database.create_table("test_exchange", "1h", is_crypto=True)
    assert table_class.__tablename__ == "test_exchange-1h"


def test_add_data(database, table):
    """
    Test adding data to a table.
    """
    data = {
        "date_time": datetime(2023, 4, 16, 12, 0, 0),
        "asset_id": "BTC",
        "base_currency": "BTC",
        "quote_currency": "USDT",
        "open": 60000,
        "high": 60500,
        "low": 59500,
        "close": 60100,
        "volume": 1200,
    }
    database.add_data(data, table)
    assert database.db_session.query(table).count() == 1


def test_query_data(database, table):
    """
    Test querying data from a table.
    """
    data = {
        "date_time": datetime(2023, 4, 16, 12, 0, 0),
        "asset_id": "BTC",
    }
    result = database.query_data(table, filters=data)
    assert len(result) == 1
    assert result[0].open == 60000
    assert result[0].high == 60500
    assert result[0].low == 59500
    assert result[0].close == 60100
    assert result[0].volume == 1200


def test_update_data(database, table):
    """
    Test updating data in a table.
    """
    filters = {
        "date_time": datetime(2023, 4, 16, 12, 0, 0),
        "asset_id": "BTC",
    }
    new_values = {"high": 61000, "low": 59000}
    database.update_data(table, filters, new_values)
    updated_data = database.query_data(table, filters=filters)
    assert updated_data[0].high == 61000
    assert updated_data[0].low == 59000


def test_remove_data_in_range(database, table):
    """
    Test removing data from a table within a given datetime range.
    """
    start_datetime = datetime(2023, 4, 16, 11, 0, 0)
    end_datetime = datetime(2023, 4, 16, 13, 0, 0)
    database.remove_data_in_range(table, start_datetime, end_datetime)
    assert database.db_session.query(table).count() == 0
