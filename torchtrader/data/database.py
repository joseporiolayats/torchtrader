"""
This script provides a module for managing a SQLite database using SQLAlchemy ORM.
The database is designed to store asset data from different exchanges and timeframes
for use in the Torchtrader application.

The main class, TorchtraderDatabase, is responsible for creating, connecting,
and managing the database. It also provides methods for adding, updating, querying,
and removing data from the tables.

The ExchangeBase class is a base class for creating exchange-specific tables that
inherit its attributes and methods.
"""
import os
from datetime import datetime
from typing import Dict
from typing import Type
from typing import Union

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from torchtrader.logs.logger import app_logger

Base = declarative_base()
TIMEFRAMES = [
    "1m",
    "3m",
    "5m",
    "10m",
    "15m",
    "30m",
    "1h",
    "3h",
    "6h",
    "12h",
    "1d",
    "3d",
    "5d",
    "1w",
    "2w",
    "1M",
    "3M",
    "6M",
    "1y",
]


class ExchangeBase(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime, nullable=False)
    asset_id = Column(String, nullable=False)
    base_currency = Column(String, nullable=False)
    quote_currency = Column(String, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)


class TorchtraderDatabase:
    """
    TorchtraderDatabase is a class for managing the SQLite database.
    It provides methods for creating, connecting, and managing the database
    as well as adding, updating, querying, and removing data from the tables.
    Attributes:
        database_uri (str): The URI of the database.
        db_session (Session): The database session object.
        db_engine (Engine): The database engine object.

    Usage:
        database = TorchtraderDatabase()
        database.connect_database()
        database.test_db()
        database.close_session()
    """

    def __init__(self, database_uri: str = "sqlite:///torchtrader.db"):
        """
        Initializes a new TorchtraderDatabase object.

        Args:
            database_uri (str): The URI of the database. Default is "sqlite:///torchtrader.db".
        """
        self.database_uri = database_uri
        self.db_session = None
        self.db_engine = None

    @staticmethod
    def create_table(exchange: str, timeframe: str, is_crypto: bool = True) -> Base:
        """
        Creates a new table class for the specified exchange and timeframe.

        Args:
            exchange (str): The name of the exchange.
            timeframe (str): The timeframe for the data.
            is_crypto (bool): Whether the asset is a cryptocurrency. Default is True.

        Returns:
            Base: The newly created table class.

        Raises:
            AssertionError: If the specified timeframe is not in the list of allowed timeframes.
        """
        assert (
            timeframe in TIMEFRAMES
        ), f"Invalid timeframe '{timeframe}'. Must be one of: {', '.join(TIMEFRAMES)}"
        table_name = f"{exchange}-{timeframe}"
        class_name = f"{exchange.capitalize()}_{timeframe.capitalize()}"
        return type(
            class_name,
            (ExchangeBase,),
            {
                "__tablename__": table_name,
                "is_crypto": Column(Integer, nullable=False, default=int(is_crypto)),
            },
        )

    def create_database(self, database_uri: str = "sqlite:///torchtrader.db") -> None:
        """
        Creates a new SQLite database.

        Args:
            database_uri (str): The URI of the database. Default is "sqlite:///torchtrader.db".
        """
        self.db_engine = create_engine(database_uri)
        session_factory = sessionmaker(bind=self.db_engine)
        self.db_session = session_factory()
        app_logger.info(f"Created new SQLite database: {database_uri}")

    def check_and_create_db(self, database_uri="sqlite:///torchtrader.db") -> None:
        """
        Checks if the specified database exists, and if not, creates it.

        Args:
            database_uri (str): The URI of the database. Default is "sqlite:///torchtrader.db".
        """
        app_logger.info(f"Checking if database {database_uri} exists")
        db_file_path = database_uri.split("///")[-1]

        if os.path.isfile(db_file_path):
            app_logger.info("Database already exists")
            self.db_engine = create_engine(database_uri)
            session_factory = sessionmaker(bind=self.db_engine)
            self.db_session = session_factory()
        else:
            app_logger.info("Database not found, creating it")
            self.create_database(database_uri)
            app_logger.info("Database created successfully")

    def add_data(
        self, data: Union[Dict[str, any], Dict[str, Dict[str, any]]], table: Type[Base]
    ) -> None:
        """
        Adds data to the specified table.

        Args:
            data (Union[Dict[str, any], Dict[str, Dict[str, any]]]): The data to be added.
            table (Type[Base]): The table class where the data will be added.

        Raises:
            ValueError: If the data is not a dictionary or a dictionary of dictionaries.
        """
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary or a dictionary of " "dictionaries")
        inserted_ids = []
        if not all(isinstance(value, dict) for value in data.values()):
            return self.add_single_datapoint(table, data, inserted_ids)
        app_logger.info(f"Adding bulk data to table {table.__tablename__}")
        for item in data.values():
            new_entry = table(**item)
            self.db_session.add(new_entry)
            inserted_ids.append(new_entry.id)

    def add_single_datapoint(self, table, data, inserted_ids) -> None:
        """
        Adds a single data point to the specified table.

        Args:
            table (Type[Base]): The table class where the data will be added.
            data (Dict[str, any]): The data to be added.
            inserted_ids (List[int]): The list of inserted primary key ids.

        Returns:
            List[int]: The list of inserted primary key ids.
        """
        app_logger.info(f"Adding single data to table {table.__tablename__}")
        new_entry = table(**data)
        self.db_session.add(new_entry)
        inserted_ids.append(new_entry.id)
        self.db_session.commit()
        app_logger.info(
            f"Data added to table {table.__tablename__} with primary keys {inserted_ids}"
        )
        return inserted_ids

    def test_db(self) -> None:
        """
        Tests the database by adding and removing sample data.
        """
        app_logger.info("Starting database test")
        binance_table = self.create_table("test_binance", "1h", is_crypto=True)
        yahoo_table = self.create_table("test_yahoo", "5m", is_crypto=False)
        Base.metadata.create_all(self.db_engine)
        data_bulk = {
            "binance_data": {
                "date_time": datetime(2023, 4, 16, 12, 0, 0),
                "asset_id": "BTC",
                "base_currency": "BTC",
                "quote_currency": "USDT",
                "open": 60000,
                "high": 60500,
                "low": 59500,
                "close": 60100,
                "volume": 1200,
            },
            "yahoo_data": {
                "date_time": datetime(2023, 4, 16, 12, 0, 0),
                "asset_id": "AAPL",
                "base_currency": "AAPL",
                "quote_currency": "USD",
                "open": 150,
                "high": 151,
                "low": 148,
                "close": 149,
                "volume": 10000,
            },
        }
        self.add_data(data_bulk, binance_table)
        self.add_data(data_bulk, yahoo_table)
        app_logger.info("Test tables added successfully")
        self.remove_table(binance_table)
        self.remove_table(yahoo_table)
        app_logger.info("Test tables dropped successfully")
        app_logger.info("Finished database test")

    def remove_table(self, table: Type[Base]) -> None:
        """
        Removes the specified table from the database.

        Args:
            table (Type[Base]): The table class to be removed.
        """
        app_logger.info(f"Removing table '{table.__tablename__}' from the database")
        table.__table__.drop(self.db_engine)
        app_logger.info(f"Table '{table.__tablename__}' removed successfully")

    def remove_data_in_range(
        self, table: Type[Base], start_datetime: datetime, end_datetime: datetime
    ) -> None:
        """
        Removes data from the specified table within a given datetime range.

        Args:
            table (Type[Base]): The table class where data will be removed.
            start_datetime (datetime): The start datetime of the range.
            end_datetime (datetime): The end datetime of the range.
        """
        app_logger.info(
            f"Removing data from table '{table.__tablename__}' between "
            f"{start_datetime} and {end_datetime}"
        )
        self.db_session.query(table).filter(
            table.datetime >= start_datetime, table.datetime <= end_datetime
        ).delete()
        self.db_session.commit()
        app_logger.info(
            f"Data removed successfully from table '{table.__tablename__}'"
            f"between {start_datetime} and {end_datetime}"
        )

    def connect_database(self, database_uri: str = "sqlite:///torchtrader.db") -> None:
        """
        Connects to the specified database or creates it if it doesn't exist.

        Args:
            database_uri (str): The URI of the database. Default is "sqlite:///torchtrader.db".
        """
        app_logger.info(f"Connecting to database '{database_uri}'")
        self.check_and_create_db(database_uri)
        app_logger.info(f"Connected to database '{database_uri}' successfully")

    def close_session(self) -> None:
        """
        Closes the current database session.
        """
        self.db_session.close()
        app_logger.info("Database session closed")

    def execute_sql(self, sql: str) -> None:
        """
        Executes the specified SQL command.

        Args:
            sql (str): The SQL command to be executed.
        """
        self.db_session.execute(sql)
        self.db_session.commit()
        app_logger.info(f"Executed SQL command: {sql}")

    def backup_database(self, backup_path: str) -> None:
        """
        Creates a backup of the database.

        Args:
            backup        backup_path (str): The path where the backup will be saved.
        """
        import shutil

        shutil.copy2(self.database_uri.split("///")[-1], backup_path)
        app_logger.info(f"Database backed up to {backup_path}")

    def restore_database(self, backup_path: str) -> None:
        """
        Restores the database from the specified backup.

        Args:
            backup_path (str): The path of the backup file.
        """
        import shutil

        shutil.copy2(backup_path, self.database_uri.split("///")[-1])
        app_logger.info(f"Database restored from {backup_path}")

    def query_data(self, table: Type[Base], filters: Dict[str, any] = None) -> None:
        """
        Queries data from the specified table with optional filters.

        Args:
            table (Type[Base]): The table class to query data from.
            filters (Dict[str, any], optional): A dictionary of filters to apply. Default is None.

        Returns:
            List[Base]: A list of rows matching the filters.
        """
        query = self.db_session.query(table)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(table, key) == value)
        return query.all()

    def update_data(
        self, table: Type[Base], filters: Dict[str, any], new_values: Dict[str, any]
    ) -> None:
        """
        Updates data in the specified table with the given filters and new values.

        Args:
            table (Type[Base]): The table class to update data in.
            filters (Dict[str, any]): A dictionary of filters to apply.
            new_values (Dict[str, any]): A dictionary of new values to update the data with.
        """
        self.db_session.query(table).filter_by(**filters).update(new_values)
        self.db_session.commit()
        app_logger.info(
            f"Updated data in table {table.__tablename__} with filters {filters}"
            f" and new values {new_values}"
        )


if __name__ == "__main__":
    database = TorchtraderDatabase()
    database.connect_database()
    database.test_db()
    database.close_session()
