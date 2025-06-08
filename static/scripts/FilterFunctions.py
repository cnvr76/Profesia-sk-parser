from typing import Callable, Tuple, Dict, List, Any

class FilterFunctions:
    def __init__(self, executeQuery: Callable):
        self.executeQuery = executeQuery

    def get_applied_to(self) -> Dict[str, Any]:
        query: str = """
            SELECT avi.*
            FROM AllVacanciesInfo avi
            JOIN VacanciesMetadata vm ON vm.V_id = avi.V_id
            WHERE vm.applied = 1
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
            WHERE Date BETWEEN DATEADD(day, -3, GETDATE()) AND GETDATE()
            ORDER BY Date desc
        """
        return self.executeQuery(query)["view"]
        