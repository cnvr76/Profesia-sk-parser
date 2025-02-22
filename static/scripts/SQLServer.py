import pyodbc
import os
from typing import Tuple, List, Dict
from static.scripts.DatabaseFunctions import Functions


class Connector(Functions):
    def __init__(self):
        super().__init__(self.executeQuery)

        self.connected: bool = False
        self.cursor: pyodbc.Cursor = None
        self.connection: pyodbc.Connection = None
    
    def connect(self) -> bool:
        driver_name: str = "ODBC Driver 17 for SQL Server"
        server_name: str = os.getenv("SERVER_NAME_SQLSERVER")
        database_name: str = os.getenv("DATABASE_NAME_SQLSERVER")
        try:
            connection_string: str = f"""
                Driver={driver_name};
                Server={server_name};
                Database={database_name};
                Trusted_Connection=yes;
            """
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            self.connection = connection
            self.cursor = cursor
            self.connected = True

            return True
        except Exception as e:
            print(e)
            self.close()
            return False
        
    def close(self):
        if self.cursor is not None and self.connected:
            self.connected = False
            self.cursor.close()
            self.connection.close()
        
    def executeQuery(self, query: str, params: Tuple = ()) -> Dict[str, List[Tuple | Dict]] | bool:
        try:
            self.cursor.execute(query, params)

            if self.cursor.description:
                cols: List[str] = [desc[0] for desc in self.cursor.description]
                rows: List[pyodbc.Row] = self.cursor.fetchall()
                return {"view": self._format(cols, rows), "sqlite": rows}
            else:
                # For INSERT, UPDATE, DELETE queries, commit the transaction
                self.connection.commit()
                print('Query executed successfully')
                return True
        except Exception as e:
            print("Error executing query:", e)
            return False

    def _format(self, cols: List[str], rows: List[pyodbc.Row]) -> List[Dict[str, object]]:
        result = []
        for row in rows:
            formatted = {cols[i]: row[i] for i in range(len(cols))}
            result.append(formatted)
        return result