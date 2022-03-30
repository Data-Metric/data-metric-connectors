from __future__ import annotations

from typing import Dict, List

import loguru

from data_metric_connector.connectors.mongo.connect import ConnectMongo
from data_metric_connector.utils.file_size import convert_size


class Mongo:
    def __init__(self, logger: loguru.Logger):
        self.logger = logger

    def get_meta(
        self, username: str, password: str, host: str, port: int, db: str
    ) -> List[Dict[str, Dict[str, str]]]:
        """
        Gets the metadata of the mongo db database.

        :param username: username of db
        :param password: password of the username
        :param host: host name of mongo db
        :param port: port number of mongo db
        :param db: mogo db database name
        :return: metadata of the database
        """
        try:
            meta = []
            client = ConnectMongo(self.logger).connect_database(
                username, password, host, port, db
            )
            for dbs in client.list_databases():
                data = client.get_database(dbs["name"]).command("dbstats")
                data.update({"avgObjSize": convert_size(data["avgObjSize"])})
                data.update({"dataSize": convert_size(data["dataSize"])})
                data.update({"storageSize": convert_size(data["storageSize"])})
                data.update({"indexSize": convert_size(data["indexSize"])})
                data.update({"totalSize": convert_size(data["totalSize"])})
                data.update({"fsUsedSize": convert_size(data["fsUsedSize"])})
                data.update({"fsTotalSize": convert_size(data["fsTotalSize"])})
                coll_info = {}
                for collections in client.get_database(
                    dbs["name"]
                ).list_collection_names():
                    collection = client.get_database(dbs["name"]).command(
                        "collStats", collections
                    )
                    coll_info[collections] = {
                        "count": collection["count"],
                        "storageSize": convert_size(collection["storageSize"]),
                    }
                data["collections"] = coll_info
                meta.append(data)
            self.logger.info(f"MetaData is {meta}")
            ConnectMongo(self.logger).disconnect_database(client)
            return meta
        except Exception as e:
            self.logger.error(f"get_meta failed with Exception - {e}")
            return []
