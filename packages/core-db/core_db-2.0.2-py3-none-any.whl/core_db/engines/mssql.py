# -*- coding: utf-8 -*-

import pyodbc

from core_db.interfaces.base import DatabaseClientException
from core_db.interfaces.sql_based import SqlDatabaseClient


class MsSqlClient(SqlDatabaseClient):
    """
    Client for Microsoft MsSQL connection...

    Example WITH context manager:
        with MsSqlClient(
            dsn="DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=master;UID=SA;PWD=sOm3str0ngP@33w0rd;Encrypt=no",
            autocommit=True,
            timeout=5
        ) as client:
            client.execute("SELECT @@VERSION AS 'version';")
            print(list(client.fetch_records()))
    """

    def __init__(self, **kwargs):
        """
        Expected -> dsn, autocommit, timeout

        More information:
            - https://learn.microsoft.com/en-us/sql/connect/python/python-driver-for-sql-server?view=sql-server-ver16
            - https://learn.microsoft.com/en-us/sql/relational-databases/native-client/applications/using-connection-string-keywords-with-sql-server-native-client?view=sql-server-ver15&viewFallbackFrom=sql-server-ver16
        """

        super(MsSqlClient, self).__init__(**kwargs)
        self.connect_fcn = pyodbc.connect

    @classmethod
    def registered_name(cls) -> str:
        return cls.__name__

    def connect(self) -> None:
        try:
            self.cxn = self.connect_fcn(
                self.cxn_parameters.pop("dsn", ""),
                **self.cxn_parameters)

        except Exception as error:
            raise DatabaseClientException(error)

    def test_connection(self, query: str = None):
        query = query or "SELECT @@VERSION AS 'version';"
        return super(MsSqlClient, self).test_connection(query)
