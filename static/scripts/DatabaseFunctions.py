from typing import Callable

class Functions:
    def __init__(self, executeQuery: Callable):
        self.executeQuery = executeQuery

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