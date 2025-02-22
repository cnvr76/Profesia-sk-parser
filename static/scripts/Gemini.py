import google.generativeai as genai
import simplejson as json
from typing import List, Dict
import os

class Gemini:
    def __init__(self):
        self.token = os.getenv("GEMINI_TOKEN")
        genai.configure(api_key=self.token)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.response_file = "db/ai_response.json"
        self.template_file = "db/json_template.json"

    def ask(self, prompt: str) -> Dict[str, List[str] | str | None]:
        response: str = self.model.generate_content(prompt).text
        formatted: str = response.replace("```json", "").replace("```", "").strip()

        with open(self.response_file, "w", encoding="utf-8") as file:
            file.write(formatted)

        return self.load_json_answer()

    def load_json_answer(self) -> Dict[str, List[str] | str | None]:
        json_answer: Dict = {}
        with open(self.response_file, "r", encoding="utf-8") as file:
            json_answer = json.load(file)
        return json_answer

    def make_prompt(self, question: str, context: str) -> str:
        json_template = open(self.template_file, "r", encoding="utf-8").read()
        prompt = f"""QUESTION:\n {question} 
                        (Then, detail the answers in JSON format like this (but with different info): {json_template}):\n 
                        CONTEXT:\n
                        '{context}'
                    """
        return prompt
