from typing import Callable, Tuple, Dict, List, Any

class FilterFunctions:
    def __init__(self, executeQuery: Callable):
        self.executeQuery = executeQuery

    def get_problematic_vacancies(self):
        query: str = """
            SELECT avi.*
            FROM AllVacanciesInfo avi
            LEFT JOIN Knowledges k ON avi.V_id = k.V_id
            LEFT JOIN Frameworks f ON avi.V_id = f.V_id
            WHERE avi.V_id IN (
                SELECT V_id FROM VacanciesMetadata
                WHERE summary IS NOT NULL
			) AND k.K_id IS NULL
        """
        return self.executeQuery(query)["view"]

    def get_applied_to(self) -> Dict[str, Any]:
        query: str = """
            SELECT avi.*
            FROM AllVacanciesInfo avi
            JOIN VacanciesMetadata vm ON vm.V_id = avi.V_id
            WHERE vm.applied = 1
        """
        return self.executeQuery(query)["view"]
    
    def get_fetched_vacancies(self):
        query: str = """
            SELECT avi.*
            FROM AllVacanciesInfo avi
            JOIN VacanciesMetadata vm ON vm.V_id = avi.V_id
            WHERE vm.summary IS NOT NULL
            ORDER BY avi.Date desc
        """
        return self.executeQuery(query)["view"]

    def get_expired(self) -> Dict[str, Any]:
        query: str = """
            SELECT avi.*
            FROM AllVacanciesInfo avi
            JOIN VacanciesMetadata vm ON vm.V_id = avi.V_id
            WHERE vm.expired = 1
        """
        return self.executeQuery(query)["view"]
    
    def get_most_recent(self) -> Dict[str, Any]: 
        query: str = """
            SELECT *
            FROM AllVacanciesInfo
            WHERE Date BETWEEN DATEADD(day, -10, GETDATE()) AND GETDATE()
            ORDER BY Date desc
        """
        return self.executeQuery(query)["view"]
        