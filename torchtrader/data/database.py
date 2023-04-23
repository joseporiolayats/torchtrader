"""
database.py
"""
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type

from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

from torchtrader.logs.logger import app_logger


class Base(DeclarativeBase):
    _decl_class_registry = None
    date_time = None
    id: int


# Define Asset model
class Asset(Base):
    __tablename__ = "assets"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    asset_id: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    base_currency: Mapped[str] = mapped_column(String(20), nullable=False)
    quote_currency: Mapped[str] = mapped_column(String(20), nullable=False)
    is_crypto: Mapped[int] = mapped_column(Integer(), nullable=False, default=1)
    data_points = relationship("DataPoint", back_populates="asset")


# Define DataPoint model
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


# TorchtraderDatabase class to manage database operations
class TorchtraderDatabase:
    """
    Initialize the TorchtraderDatabase and create tables if they don't exist.
    """

    def __init__(self):
        db_path = "torchtrader/data/torchtrader.db"
        db_filename = "torchtrader.db"
        self.database_uri = (
            Path(db_path).absolute()
            if Path(db_path).absolute().exists()
            else Path(db_filename).absolute()
        )
        self.db_engine = create_engine(f"sqlite:///{self.database_uri}")
        self.db_session = Session(self.db_engine)

        app_logger.info("Database created successfully")

        Base.metadata.create_all(bind=self.db_engine)

    def add_asset(self, asset: Dict[str, Any]) -> int | None:
        """
        Add an asset to the database.

        Args:
            asset (Dict[str, Any]): A dictionary containing the asset details.

        Returns:
            int: The ID of the added asset.
        """
        try:
            new_asset = Asset(**asset)
            self.db_session.add(new_asset)
            self.db_session.commit()
            app_logger.info(f"Asset added: {new_asset.asset_id}")
            return new_asset.id
        except Exception as e:
            app_logger.error(f"Error adding asset: {e}")
            self.db_session.rollback()
            return None

    def add_data_points(self, asset_id: int, data_points: List[Dict[str, Any]]) -> List[int]:
        """
        Add data points to the database for a given asset.

        Args:
            asset_id (int): The ID of the asset for which to add data points.
            data_points (List[Dict[str, Any]]): A list of dictionaries containing data points.

        Returns:
            List[int]: A list of IDs of the added data points.
        """

        try:
            new_data_points = [
                DataPoint(asset_id=asset_id, **data_point) for data_point in data_points
            ]
            self.db_session.add_all(new_data_points)
            self.db_session.commit()
            app_logger.info(f"{len(new_data_points)} data points added for asset_id {asset_id}")
            return [data_point.id for data_point in new_data_points]
        except Exception as e:
            app_logger.error(f"Error adding data points: {e}")
            self.db_session.rollback()
            return []

    def query_data_points(self, asset_id: int, filters: Dict[str, Any] = None) -> List[DataPoint]:
        """
        Query data points for a given asset with optional filters.

        Args:
            asset_id (int): The ID of the asset for which to query data points.
            filters (Dict[str, Any], optional): A dictionary of filters to apply to the query.
            Defaults to None.

        Returns:
            List[DataPoint]: A list of DataPoint objects matching the query.
        """

        try:
            stmt = select(DataPoint).where(DataPoint.asset_id == asset_id)

            if filters:
                for key, value in filters.items():
                    stmt = stmt.where(getattr(DataPoint, key) == value)

                with self.db_session as session:
                    result = session.execute(stmt)
                    data_points = result.scalars().all()
                    app_logger.info(
                        f"Queried {len(data_points)} data points for asset_id {asset_id}"
                    )
                    return [DataPoint(**dp.__dict__) for dp in data_points]

        except Exception as e:
            app_logger.error(f"Error querying data points: {e}")
        return []

    def get_asset(self, asset_id: str) -> Optional[Dict[str, Any]]:
        """
        Get an asset by its asset_id.

        Args:
            asset_id (str): The asset_id of the asset to retrieve.

        Returns:
            Optional[Dict[str, Any]]:
            A dictionary containing the asset details if found, None otherwise.
        """
        try:
            asset = self.get_single(Asset, {"asset_id": asset_id})
            if asset:
                app_logger.info(f"Retrieved asset: {asset_id}")
            else:
                app_logger.warning(f"Asset not found: {asset_id}")
            return asset
        except Exception as e:
            app_logger.error(f"Error getting asset: {e}")
            return None

    def close_session(self) -> None:
        """
        Close the database session.
        """

        self.db_session.close()
        app_logger.info("Database session closed")

    def get_single(self, Model: Type[Base], param: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get a single record of a given model matching the provided parameters.

        Args:
            Model (Type[Base]): The SQLAlchemy model to query.
            param (Dict[str, Any]): A dictionary of parameters to filter the query.

        Returns:
            Optional[Dict[str, Any]]:
            A dictionary containing the record details if found, None otherwise.
        """
        try:
            return self.db_session.query(Model).filter_by(**param).first()
        except Exception as e:
            app_logger.error(f"Error getting single record: {e}")
            return None

    def run_query(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Executes an SQL query using SQLAlchemy and returns the result as a list of dictionaries.

        Args:
            query (str): SQL query string to execute.
            params (Dict[str, Any], optional): Dictionary of parameters to be passed with the query.
            Defaults to None.

        Returns:
            List[Dict[str, Any]]: List of dictionaries with the query result.
        """
        try:
            if params is None:
                params = {}
            query = text(query)
            result_proxy = self.db_session.execute(query, params)
            app_logger.info(f"Executed query: {query}")
            return [dict(row) for row in result_proxy.fetchall()]
        except Exception as e:
            app_logger.error(f"Error executing query: {e}")
            return []


if __name__ == "__main__":
    database = TorchtraderDatabase()
    database.close_session()
