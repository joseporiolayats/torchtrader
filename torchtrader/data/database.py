"""
torchtrader/data/database.py
"""
from typing import Any
from typing import Dict
from typing import List
from typing import Type

from sqlalchemy import and_
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import FlushError

from torchtrader.data.schema import Base
from torchtrader.logs.logger import app_logger
from torchtrader.utils import find_dir
from torchtrader.utils import find_file


class GenericDatabase:
    def __init__(self, db_path: str = None):
        db_path = "torchtrader/data/torchtrader.db" if db_path is None else db_path
        self.db_filename = db_path.split("/")[-1]

        self.database_uri = self.locate_or_create_db()

        self.db_engine = create_engine(f"sqlite:///{self.database_uri}")
        self.db_session = Session(self.db_engine)

        app_logger.info("Database connected successfully.")

        Base.metadata.create_all(bind=self.db_engine)

    def locate_or_create_db(self):
        locate = find_file(self.db_filename)
        if locate is not None:
            app_logger.info(f"Database found in {locate}")
            return locate
        default_location = find_dir("data") / self.db_filename
        app_logger.info(f"Database created successfully in {default_location}")
        return default_location

    def create(self, tableclass: Type[Base], data: Dict[str, Any]) -> int | None:
        # sourcery skip: extract-duplicate-method, use-named-expression
        try:
            # Check if the record with the same data already exists in the database
            exists = (
                self.db_session.query(tableclass)
                .filter(
                    and_(
                        *[
                            getattr(tableclass, key) == value
                            for key, value in data.items()
                            if value is not None
                        ]
                    )
                )
                .first()
            )

            if exists:
                app_logger.warning(
                    f"{tableclass.__name__} with data {data} " f"already exists. Skipping creation."
                )
                return None

            record = tableclass(**data)
            self.db_session.add(record)
            self.db_session.commit()
            app_logger.info(f"Created {tableclass.__name__} with data: {data}")
            return record.id
        except (IntegrityError, FlushError) as e:
            app_logger.error(f"Error creating {tableclass.__name__}: {e}")
            self.db_session.rollback()
            return -1
        except Exception as e:
            app_logger.error(f"Unexpected error creating {tableclass.__name__}: {e}")
            self.db_session.rollback()
            return None

    def read(self, tableclass: Type[Base], filters: Dict[str, Any] = None) -> List[Type[Base]]:
        try:
            query = self.db_session.query(tableclass)

            if filters:
                query = query.filter_by(**filters)

            records = query.all()
            app_logger.info(f"Read {len(records)} records from {tableclass.__name__}")
            return records
        except Exception as e:
            app_logger.error(f"Error reading {tableclass.__name__}: {e}")
            return []

    def update(
        self, tableclass: Type[Base], record: Dict[str, Any], updates: Dict[str, Any]
    ) -> None:
        # sourcery skip: use-named-expression
        try:
            target_record = self.db_session.query(tableclass).filter_by(**record).first()

            if target_record is None:
                app_logger.warning(f"Record not found in {tableclass.__name__}. Skipping.")
                return

            for key, value in updates.items():
                # Check if the updated value is already present in the database
                exists = (
                    self.db_session.query(tableclass)
                    .filter(
                        and_(
                            getattr(tableclass, key) == value,
                            tableclass.id != target_record.id,
                        )
                    )
                    .first()
                )

                if exists:
                    app_logger.warning(
                        f"{tableclass.__name__} with {key}={value} already exists. Skipping update."
                    )
                    continue

                setattr(target_record, key, value)

            self.db_session.commit()
            app_logger.info(f"Updated {tableclass.__name__} with record {record}")
        except (IntegrityError, FlushError) as e:
            app_logger.error(f"Error updating {tableclass.__name__} with " f"record {record}: {e}")
            self.db_session.rollback()
        except Exception as e:
            app_logger.error(
                f"Unexpected error updating {tableclass.__name__} with " f"record {record}: {e}"
            )
            self.db_session.rollback()

    def delete(self, tableclass: Type[Base], data: Dict[str, Any]) -> None:
        try:
            target_record = self.db_session.query(tableclass).filter_by(**data).first()

            if not target_record:
                app_logger.warning(f"Item {data} doesn't exist in {tableclass.__name__}. Skipping.")
                return

            self.db_session.delete(target_record)
            self.db_session.commit()
            app_logger.info(f"Deleted {tableclass.__name__} with {data}")
        except Exception as e:
            app_logger.error(f"Error deleting {tableclass.__name__} with " f"record {data}: {e}")
            self.db_session.rollback()

    def close(self):
        self.db_session.close()
        app_logger.info("Database session closed.")
