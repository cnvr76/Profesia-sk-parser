from static.scripts.Parser import Parser
from typing import List, Dict, Tuple
import logging

class ParserService:
    def __init__(self) -> None:
        self.__query_params = {
            "newer_than": (5, "day"),
            "older_than": (1, "day"),
            "sender": "support@profesia.sk"
        }
        self.__parser = Parser(self.__query_params)
    
    @property
    def conn(self):
        return self.__parser.connector
    @property
    def ai(self):
        return self.__parser.ai
    @property
    def engine(self):
        return self.__parser

    def get_vacancy_details(self, v_id: int) -> Dict:
        try:
            self.conn.connect()

            data: Dict = self.conn.get_vacancy_by_id(v_id)

            # Getting info for the vacancy
            last_response: Dict[str, Dict] = self.engine.read_from_json(self.engine.json_last_response)
            response: Dict[str, Dict] = last_response
            detailsExist: bool = data.get("Salary") is not None
            answer: Dict = {}

            if v_id == last_response["v_id"]:
                answer = self.ai.load_json_answer()
            # If the row has any type of the missing data
            elif detailsExist:
                answer = self.conn.get_vacancy_metadata(v_id)
            else:
                response = self.engine.send_request(v_id, link=data["Link"])
                prompt: str = self.ai.make_prompt(
                    question="Что мне нужно знать для этой вакансии (на словацком) + зарплату бери минимальную и одним числом",
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
        except Exception as e:
            return {f"error ({__name__})": str(e)}
        finally:
            self.conn.close()

    def delete_vacancy(self, v_id: int):
        try:
            self.conn.connect()
            success: bool = self.conn.delete_vacancy(v_id)
            return {"executed": success}
        except Exception as e:
            return {"executed": False, "error": str(e)}
        finally:
            self.conn.close()

    def star_vacancy(self, v_id: int):
        try:
            self.conn.connect()

            result: Dict[str, List] = self.conn.executeQuery("SELECT V_id FROM Starred WHERE V_id = ?", (v_id,))
            exists: bool = bool(result.get("view"))

            if exists:
                executed: bool = self.conn.remove_from_starred(v_id)
                isStarred: bool = False 
            else:
                executed: bool = self.conn.add_to_starred(v_id)
                isStarred: bool = True
            
            return {"executed": executed, "starred": isStarred}
        except Exception as e:
            return {f"error ({__name__})": str(e)}
        finally:
            self.conn.close()

parser_service: ParserService = ParserService()