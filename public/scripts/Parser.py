import re
from pprint import pprint
import sqlite3
from typing import List, Dict, Tuple, Set, Awaitable

import requests
import simplejson as json
from bs4 import BeautifulSoup
from simplegmail import Gmail
from simplegmail.query import construct_query

from public.scripts.Database import Connector
from public.scripts.Gemini import Gemini


class Parser:
    def __init__(self, query_params: Dict):
        self.gmail = Gmail(client_secret_file="tokens/client_secret.json")
        self.query_params: Dict = query_params
        self.messages: List = []
        self.vacancies: Dict[str, Dict] = {}
        self.json_file = "db/vacancies.json"

        self.ai = Gemini(token="tokens/gemini_token.txt")

        self.db = Connector()

    def get_messages(self) -> List:
        return self.gmail.get_messages(query=construct_query(self.query_params))

    def parse_messages(self, messages: List) -> Dict[str, Dict]:
        self.messages = messages
        for msg in self.messages:
            soup = BeautifulSoup(msg.html, "html.parser")
            vacancy: Dict[str, Dict] = {}

            search_link = 'profesia.sk/lnk'
            offers = soup.find_all("a", href=re.compile(search_link))

            parents = []
            for o in offers:
                parent = o.find_parent("td")
                if parent:
                    parents.append(parent)

            for offer in parents:
                # Найти тег <a>
                a_tag = offer.find("a", href=True)
                if not a_tag:
                    continue

                # Найти div с информацией
                div_tag = offer.find("div")
                if not div_tag:
                    continue

                info = div_tag.text.strip().split("\n")
                info = [a.strip() for a in info if a.strip()]

                # Убедимся, что информация содержит минимум два элемента
                if len(info) < 2:
                    continue

                # Собираем данные
                position: str = a_tag.text.strip()
                link: str = a_tag["href"]
                company: str = info[0].replace("'", "`")
                location: str = info[1] if len(info) > 1 else "Unknown"

                vacancy[position] = {"link": link, "company": company, "location": location}

            self.vacancies[msg.date] = vacancy
        return self.vacancies

    # TODO - Сделать проверку но то, что уже есть в дб, после чего записать новую инфурмацию
    def write_to_db(self, vacancies: Dict[str, Dict]) -> Awaitable[bool]:
        # 1. insert into Companies, Locations
        # 2. select c_id from Companies
        # 3. use this info + json to insert into Vacancies

        # 1 -------------------
        # Companies inserts
        try:
            companies: Set[str] = set()
            for date, propositions in vacancies.items():
                if len(propositions) == 0:
                    continue
                for position, details in propositions.items():
                    companies.add(details["company"])

            for company in companies:
                query_companies = f"""
                    INSERT INTO Companies (Name) VALUES
                    ('{company}');
                """
                result: bool = self.db.executeQuery(query_companies)
                if not result:
                    print(f"Problem with writing: {company}")
        except sqlite3.IntegrityError as ie:
            print("Companies are already inserted!")

        # Locations inserts (code won't be used anymore)
        # try:
        #     with open("db/cities.txt", "r", encoding="utf-8") as file:
        #         cities = file.read().split("\n")
        #         for city in cities:
        #             query_companies = f"""
        #                 INSERT INTO Locations (City) VALUES
        #                 ('{city.strip()}');
        #             """
        #             result: bool = self.db.executeQuery(query_companies)
        #             if not result:
        #                 print(f"Problem with writing: {city}")
        # except sqlite3.IntegrityError as ie:
        #     print("Locations are already inserted!")
        # 2 -------------------
        view_companies: List[Tuple] = self.db.executeQuery("SELECT * FROM Companies")
        companies_sql: Dict[str, int] = {row[1]: row[0] for row in view_companies}

        view_locations: List[Tuple] = self.db.executeQuery("SELECT * FROM Locations")
        locations_sql: Dict[str, int] = {row[1]: row[0] for row in view_locations}

        locations_sql2 = locations_sql.copy()
        locations_sql2.pop("Slovensko")
        # 3 -------------------
        query_vacancies: str = "INSERT INTO Vacancies (Position, Link, Company, Location) VALUES"
        values: List[str] = []

        for date, propositions in vacancies.items():
            if len(propositions) == 0:
                continue
            for position, details in propositions.items():

                location_id = next(
                    (id for city, id in locations_sql2.items() if city in details.get("location")),
                    locations_sql["Slovensko"]
                )
                # print(location_id, details.get('location'))
                company = details['company']
                company_id: int = companies_sql.get(company, -1)
                if company_id == -1:
                    result: bool = self.db.executeQuery(f"""
                        INSERT INTO Companies (Name) VALUES
                        ('{details['company']}');
                    """)
                    if result:
                        company_id = self.db.executeQuery(
                            f"SELECT C_id FROM Companies WHERE Name = '{details['company']}'")[0][0]
                values.append(f"('{position}', '{details['link']}', {company_id}, {location_id});")
        # print(values, sep="\n")
        for i in range(len(values)):
            try:
                query: str = f"{query_vacancies} {values[i]}"
                result: bool = self.db.executeQuery(query)
                if not result:
                    print("Problem with writing this vacancy: ", values[i])
            except sqlite3.IntegrityError as ie:
                print(ie)

    def remove_duplicates(self, vacancies: Dict[str, Dict], replace: bool = False) -> Dict[str, Dict]:
        unique_vacancies: Dict[str, Dict] = {}
        seen_positions = set()
        for date, propositions in vacancies.items():
            unique_vacancies[date] = {}
            for position, details in propositions.items():
                if position not in seen_positions:
                    unique_vacancies[date][position] = details
                    seen_positions.add(position)

        if replace:
            self.vacancies = unique_vacancies
            self.write_to_json(unique_vacancies)

        return unique_vacancies

    def send_request(self, link: str, timeout: float = 2) -> Dict[str, str | bool]:
        page: requests.Request = requests.get(link, timeout=timeout)
        soup = BeautifulSoup(page.content, 'html.parser')

        haveApplied: bool = soup.find(
            text=re.compile("Na túto pracovnú ponuku ste reagovali poslaním životopisu")
        ) is not None

        job_panel = soup.find("div", attrs={"class": "panel-body"})
        job_panel_info: str = (
            "\n".join([line.strip() for line in job_panel.get_text().splitlines() if line.strip()])
            if job_panel else "No information found"
        )

        job_info = soup.find("div", attrs={"class": "details", "itemprop": "description"})
        job_info_text: str = job_info.get_text(separator="\n").strip() if job_info else "No information found"

        return {
            "header": job_panel_info,
            "details": job_info_text,
            "applied": haveApplied
        }

    def read_from_json(self, replace: bool = False) -> Dict[str, Dict]:
        with open(self.json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            if replace:
                self.vacancies = data
            return data

    def write_to_json(self, vacancies: Dict[str, Dict]) -> None:
        with open(self.json_file, "w", encoding="utf-8") as file:
            json.dump(vacancies, file, indent=4, ensure_ascii=False)
