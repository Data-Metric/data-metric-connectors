from __future__ import annotations

from typing import Dict, List

import loguru

from data_metric_connector.connectors.mysql.connect import ConnectMySql
from data_metric_connector.utils.file_size import convert_size


class MySql:
    def __init__(self, logger: loguru.Logger):
        self.logger = logger

    def get_meta(
        self, username: str, password: str, host: str, port: int, db: str
    ) -> List[Dict[str, Dict[str, str]]]:
        cxn = ConnectMySql(self.logger).connect_database(
            username, password, host, port, db
        )
        cursor = cxn.cursor(buffered=True)
        try:
            with open(
                "connectors/mysql/meta_sql/meta.sql",
                "r",
            ) as f:
                query_count = 0
                for cursors in cursor.execute(f.read(), (db, db), multi=True):
                    query_count += 1
                    result = cursors.fetchall()
                    if query_count == 1:
                        tables_size = {
                            table_name: [convert_size(int(size))]
                            for table_name, size in result
                        }
                    elif query_count == 2:
                        tables_count = {
                            table_name: [column_count, int(row_count)]
                            for table_name, column_count, row_count in result
                        }
                meta = [
                    {
                        tables: {
                            "Size": tables_size[tables][0],
                            "row_count": tables_count[tables][1],
                            "column_count": tables_count[tables][0],
                        }
                        for tables in tables_size.keys()
                    }
                ]
                self.logger.info(f"MetaData is {meta}")
            return meta
        except Exception as e:
            self.logger.error(f"Unable to execute query! - {e}")
            return []
        finally:
            cursor.close()
            ConnectMySql(self.logger).disconnect_database(cxn)
