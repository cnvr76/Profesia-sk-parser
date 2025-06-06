from typing import Callable, Tuple, List, Dict, Callable, Any
import re

class Functions:
    def __init__(self, executeQuery: Callable):
        self.executeQuery = executeQuery

    def all(self):
        query: str = """
            SELECT v.V_id, v.Position, v.Link, c.Name as 'Company', l.City as 'Location', s.S_id as 'isStarred', v.Date
            FROM Vacancies v
            JOIN Locations l ON l.L_id = v.Location
            JOIN Companies c ON c.C_id = v.Company
            LEFT JOIN Starred s ON v.V_id = s.V_id 
            ORDER BY v.Date desc
        """
        return self.executeQuery(query)["view"]
    
    def get_vacancy_by_id(self, v_id: int):
        return self.executeQuery("SELECT * FROM Vacancies WHERE V_id = ?", (v_id))["view"][0]
    
    def get_vacancy_metadata(self, v_id: int):
        query: str = """
            SELECT Salary as 'salary', Description as 'summary', 
                haveApplied as 'applied', hasExpired as 'expired' 
            FROM Vacancies
            WHERE V_id = ?
        """
        return self.executeQuery(query, (v_id,))["view"][0]
    
    def check_insert_realated_data(
            self, 
            v_id: int, 
            items: Tuple[Any], # with V_id
            table: str, 
            columns: Tuple[str], # with V_id
            value_adapter: Callable[[Any], tuple] = lambda x: (x,)
        ):
        dataExist: bool = len(
            self.executeQuery(f"SELECT * FROM {table} WHERE V_id = ?", (v_id))["rows"]) > 0

        if not dataExist:
            for item in items:
                try:
                    params = value_adapter(item)
                    questionmarks = ", ".join(("?") * len(columns))
                    self.executeQuery(f"INSERT INTO {table}({', '.join(columns)}) VALUES({questionmarks})", 
                                      (v_id, *params))
                except Exception as e:
                    return {f"error ({__name__})": str(e)}
    
    def delete_from(self, table: str):
        return self.executeQuery(f"DELETE FROM {table}")
    
    def get_full_vacancy_details(self, v_id: int):
        result = self.executeQuery("EXEC GetVacancyDetails ?", (v_id,), multi=True)
        return {
            **result[0]["view"][0],
            "Knowledges": result[1]["view"],
            "Frameworks": result[2]["view"]
        }
    
    def is_position_exists(self, position: str) -> bool:
        result = self.executeQuery("SELECT 1 FROM Vacancies WHERE Position = ?", (position,))["rows"]
        return len(result) > 0

    def remove_from_starred(self, v_id: int):
        return self.executeQuery("DELETE FROM Starred WHERE V_id = ?", (v_id,))
    
    def add_to_starred(self, v_id: int):
        return self.executeQuery("INSERT INTO Starred(V_id) VALUES(?)", (v_id,))
    
    def delete_vacancy(self, v_id: int):
        return self.executeQuery("DELETE FROM Vacancies WHERE v_id = ?", (v_id,))

    def update_vacancy_details(self, v_id: int, ai_answer: Dict, parsed_response: Dict) -> None:
        salary: int = int(''.join(re.findall(r"\d+", ai_answer.get("salary", 0))))
        params = (
            salary,
            ai_answer.get("summary"),
            int(parsed_response.get("applied", False)),
            int(parsed_response.get("expired", False)),
            v_id
        )
        return self.executeQuery("""
            UPDATE Vacancies
            SET 
                Salary = CASE WHEN Salary IS NULL THEN ? ELSE Salary END,
                Description = CASE WHEN Description IS NULL THEN ? ELSE Description END,
                haveApplied = CASE WHEN haveApplied IS NULL THEN ? ELSE haveApplied END,
                hasExpired = CASE WHEN hasExpired IS NULL THEN ? ELSE hasExpired END
            WHERE V_id = ?;
        """, params)

