from typing import Callable, Tuple, List, Dict
import re

class Functions:
    def __init__(self, executeQuery: Callable):
        self.executeQuery = executeQuery

    def all(self):
        query: str = """
            SELECT v.V_id, v.Position, v.Link, c.Name as 'Company', l.City as 'Location', s.S_id as 'isStarred'
            FROM Vacancies v
            JOIN Locations l ON l.L_id = v.Location
            JOIN Companies c ON c.C_id = v.Company
            LEFT JOIN Starred s ON v.V_id = s.V_id  
        """
        return self.executeQuery(query)
        
    
    def delete_from(self, table: str):
        return self.executeQuery(f"DELETE FROM {table}")
    
    def update_vacancy_details(self, v_id: int, answer: Dict, response: Dict) -> None:
        salary: int = int(''.join(re.findall(r"\d+", answer["salary"])))
        return self.executeQuery("""
            UPDATE Vacancies
            SET 
                Salary = CASE WHEN Salary IS NULL THEN ? ELSE Salary END,
                Description = CASE WHEN Description IS NULL THEN ? ELSE Description END,
                haveApplied = CASE WHEN haveApplied IS NULL THEN ? ELSE haveApplied END,
                hasExpired = CASE WHEN hasExpired IS NULL THEN ? ELSE hasExpired END
            WHERE V_id = ?;
        """, (salary, answer['summary'], int(response['applied']), int(response['expired']), v_id))

