import sqlite3 as sql
from typing import List, Dict, Tuple
from pprint import pprint
from static.scripts.DatabaseFunctions import Functions

class Connector(Functions):
    def __init__(self):
        self.db_name = "db/profesiask.db"
        self.connect()

        super().__init__(self.executeQuery)

    def connect(self):
        self.connection = sql.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self

    def close(self):
        self.connection.close()

    def executeQuery(self, query: str, params: Tuple=(), format: bool=True) -> List[Dict[str, int | str] | Tuple] | bool:
        try:
            self.cursor.execute(query, params)
            if self.cursor.description:
                data = self.cursor.fetchall()
                return self._format(data, self.cursor.description) if format else data
            else:
                self.connection.commit()
                print("Query executed succesfully!")
                return True
        except sql.OperationalError as oe:
            self.connection.rollback()
            print(oe)
            return False
        except sql.ProgrammingError as pe:
            print(pe)
            return [{}]
        
    def _format(self, raw_data, description) -> List[Dict[str, int | str]]:
        columns = [col[0] for col in description]
        result = []
        for row in raw_data:
            formatted = {columns[i]: row[i] for i in range(len(columns))}
            result.append(formatted)
        return result