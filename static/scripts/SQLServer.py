import pyodbc
import os
from typing import Tuple, List, Dict
from static.scripts.DatabaseFunctions import Functions
from static.scripts.FilterFunctions import FilterFunctions
import dotenv

class Connector(Functions, FilterFunctions):
    def __init__(self):
        Functions.__init__(self, self.executeQuery)
        FilterFunctions.__init__(self, self.executeQuery)

        dotenv.load_dotenv()

        self.connected: bool = False
        self.cursor: pyodbc.Cursor = None
        self.connection: pyodbc.Connection = None
    
    def connect(self) -> pyodbc.Connection:
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

            return self.connection
        except Exception as e:
            print(e)
            self.close()
            return None
        
    def close(self):
        if self.cursor is not None and self.connected:
            self.connected = False
            self.cursor.close()
            self.connection.close()
        
    def executeQuery(self, query: str, params: Tuple = None, multi: bool = False) -> Dict | List[Dict]:
        try:
            self.cursor.execute(query, params or ())
            results = []
            
            # Обработка для запросов, возвращающих данные
            if self.cursor.description:
                while True:
                    cols = [desc[0] for desc in self.cursor.description]
                    rows = self.cursor.fetchall()
                    
                    result_set = {
                        "view": self._format(cols, rows),
                        "rows": rows,
                        "cols": cols
                    }
                    
                    results.append(result_set)
                    
                    # Для multi-режима переходим к следующему набору
                    if not multi or not self.cursor.nextset():
                        break
            
            # Для запросов без возвращаемых данных (INSERT/UPDATE/DELETE)
            else:
                self.connection.commit()
                affected_rows = self.cursor.rowcount
                return {
                    "success": True,
                    "rowcount": affected_rows
                }
            
            # Возвращаем результат в зависимости от режима
            if multi:
                return results
            else:
                return results[0] if results else None
                
        except Exception as e:
            print("Error executing query:", e)
            # Откатываем транзакцию при ошибке
            if self.connection:
                self.connection.rollback()
                
            # Возвращаем информацию об ошибке в соответствующем формате
            if multi:
                return [{"error": str(e)}]
            else:
                return {"error": str(e)}

    def _format(self, cols: List[str], rows: List[pyodbc.Row]) -> List[Dict[str, object]]:
        result = []
        for row in rows:
            formatted = {cols[i]: row[i] for i in range(len(cols))}
            result.append(formatted)
        return result