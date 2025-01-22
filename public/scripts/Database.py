import sqlite3 as sql
from typing import List, Dict, Tuple

class Connector:
    def __init__(self):
        self.connection = sql.connect("db/profesiask.db")
        self.cursor = self.connection.cursor()

    def executeQuery(self, query: str) -> List[Tuple] | bool:
        try:
            self.cursor.execute(query)
            if self.cursor.description:
                return self.cursor.fetchall()
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
            return []

