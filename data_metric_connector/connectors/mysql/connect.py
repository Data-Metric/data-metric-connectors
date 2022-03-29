from __future__ import annotations

import loguru
import mysql.connector


class ConnectMySql:
    def __init__(self, logger: loguru.Logger):
        self.logger = logger

    def test_connection(
        self, username: str, password: str, host: str, port: int, db: str
    ) -> bool:
        try:
            cnx = mysql.connector.connect(
                user=username, password=password, host=host, port=port, database=db
            )
            self.logger.info("Authentication Successful! for MySql db")
            cnx.close()
            return True
        except Exception as e:
            self.logger.error(f"Authentication Failed for MySql db - {e}")
            return False

    def connect_database(
        self, username: str, password: str, host: str, port: int, db: str
    ) -> mysql.connector.connect:
        try:
            cnx = mysql.connector.connect(
                user=username, password=password, host=host, port=port, database=db
            )
            self.logger.info("MySql Database connected!")
            return cnx
        except Exception as e:
            raise Exception(f"MySql Database connection error! - {e}")

    def disconnect_database(self, cnx: mysql.connector.connect) -> None:
        try:
            cnx.close()
            self.logger.info("MySql Database disconnected!")
        except Exception as e:
            raise Exception(f"MySql Database disconnection error! - {e}")
