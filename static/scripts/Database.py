import sqlite3 as sql
from typing import List, Dict, Tuple
from pprint import pprint

class Connector:
    def __init__(self):
        self.db_name = "db/profesiask.db"
        self.connect()

    def connect(self):
        self.connection = sql.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self
    
    def all(self):
        query: str = """
            SELECT v.V_id, v.Position, v.Link, c.Name as 'Company', l.City as 'Location' 
            FROM Vacancies v
            JOIN Locations l ON l.L_id = v.Location
            JOIN Companies c ON c.C_id = v.Company
        """
        return self.executeQuery(query)
    
    def delete_from(self, table: str):
        return self.executeQuery(f"DELETE FROM {table}")

    def executeQuery(self, query: str, params: Tuple=(), format=True) -> List[Dict[str, int | str]] | bool:
        try:
            self.cursor.execute(query, params)
            # print(self.cursor.description)
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