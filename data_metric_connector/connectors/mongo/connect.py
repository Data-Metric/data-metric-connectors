from __future__ import annotations

import loguru
import pymongo
from mongoengine import connect


class ConnectMongo:
    def __init__(self, logger: loguru.Logger):
        self.logger = logger

    def test_connection(
        self, username: str, password: str, host: str, port: int, db: str
    ) -> bool:
        client = pymongo.MongoClient(
            f"mongodb://{username}:{password}@{host}:{port}/{db}"
        )
        try:
            if client[db].list_collection_names() is not None:
                self.logger.info("Authentication Successful! for mongo db")
                return True
            else:
                raise Exception("Unable to Authenticate! mongo db")
        except Exception as e:
            self.logger.error(f"Authentication Failed! for mongo db - {e}")
            return False
        finally:
            self.logger.info("Connection Getting Closed for mongo db")
            client.close()

    def connect_database(
        self, username: str, password: str, host: str, port: int, db: str
    ) -> connect:
        try:
            db = pymongo.MongoClient(
                f"mongodb://{username}:{password}@{host}:{port}/{db}"
            )
            self.logger.info("Mongo Database connected!")
            return db
        except Exception as e:
            raise Exception(f"Database connection error! - {e}")

    def disconnect_database(self, db: connect) -> None:
        try:
            db.close()
            self.logger.info("Mongo Database disconnected!")
        except Exception as e:
            raise Exception(f"Database disconnection error! - {e}")
