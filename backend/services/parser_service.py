from scripts.Parser import Parser
from typing import List, Dict, Tuple, Callable
import logging
from scripts.utilities import handle_db_connection

class ParserService:
    def __init__(self) -> None:
        self.__query_params = {
            "newer_than": (5, "day"),
            "older_than": (1, "day"),
            "sender": "support@profesia.sk"
        }
        self.__parser = Parser(self.__query_params)
        self.__filter_options: Dict[str, Callable] = {
            "all": self.load_all_data,
            "fetched": self.conn.get_fetched_vacancies,
            "applied_to": self.conn.get_applied_to,
            "expired": self.conn.get_expired,
            "most_recent": self.conn.get_most_recent,
            "problematic": self.conn.get_problematic_vacancies
        }
    
    @property
    def conn(self):
        return self.__parser.connector
    @property
    def ai(self):
        return self.__parser.ai
    @property
    def engine(self):
        return self.__parser

    @handle_db_connection
    def load_all_data(self):
        return self.conn.all()

    @handle_db_connection
    def get_vacancy_details(self, v_id: int) -> Dict:
        data: Dict = self.conn.get_vacancy_by_id(v_id)
        detailsExist: bool = self.conn.check_details_exist(v_id)

        # Getting info for the vacancy
        last_response: Dict[str, Dict] = self.engine.read_from_json(self.engine.json_last_response)
        response: Dict[str, Dict] = last_response
        answer: Dict = {}

        if v_id == last_response["v_id"]:
            answer = self.ai.load_json_answer()
        # If the row has any type of the missing data
        elif detailsExist:
            answer = self.conn.get_vacancy_metadata(v_id)
        else:
            response = self.engine.send_request(v_id, link=data["Link"], timeout=5)
            prompt: str = self.ai.make_prompt(
                question="Что конкретно мне нужно знать для этой вакансии (на словацком) + зарплату бери минимальную и одним числом",
                context=f"Header of the vacancy: {response['header']}\nBody: {response['details']}"
            )
            answer = self.ai.ask(prompt)
        
        # Writing missing info to db (table Vacancies)
        if not detailsExist:
            try:
                self.conn.update_vacancy_details(v_id, answer, response)
                pass
            except Exception as e:
                return {f"error ({__name__})": str(e)}
        
        # Writing info to db (table Knowledges)
        self.conn.check_insert_realated_data(
            v_id,
            items=answer.get("knowledge", []),
            table="Knowledges",
            columns=('V_id', 'Field', 'Description'),
            value_adapter=lambda item: (item['name'], item['description'])
        )
        self.conn.check_insert_realated_data(
            v_id,
            items=answer.get("frameworks", []),
            table="Frameworks",
            columns=('V_id', 'Name'),
        )

        # Final details of the vacancy
        details: Dict = self.conn.get_full_vacancy_details(v_id)

        return details

    @handle_db_connection
    def delete_vacancy(self, v_id: int):
        success: bool = self.conn.delete_vacancy(v_id)
        return {"executed": success}

    @handle_db_connection
    def star_vacancy(self, v_id: int):
        result: Dict[str, List] = self.conn.executeQuery("SELECT V_id FROM Starred WHERE V_id = ?", (v_id,))
        exists: bool = bool(result.get("view"))

        if exists:
            executed: bool = self.conn.remove_from_starred(v_id)
            isStarred: bool = False 
        else:
            executed: bool = self.conn.add_to_starred(v_id)
            isStarred: bool = True
        
        return {"executed": executed, "starred": isStarred}

    @handle_db_connection
    def load_newest_vacancies(self):
        messages = self.engine.get_messages()
        parsed_messages = self.engine.parse_messages(messages)
        unique_vacancies = self.engine.remove_duplicates(parsed_messages, replace=True)
        
        self.engine.write_to_db(unique_vacancies)
        return {"executed": True, "newest_data": unique_vacancies}

    @handle_db_connection
    def filter_vacancies(self, filter_name: str):
        filter_function: Callable = self.__filter_options.get(filter_name, lambda: [{}])
        return filter_function()

parser_service: ParserService = ParserService()