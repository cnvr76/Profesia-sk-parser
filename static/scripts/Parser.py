import re
from pprint import pprint
import sqlite3
from typing import List, Dict, Tuple, Set, Awaitable

import requests
import simplejson as json
from bs4 import BeautifulSoup
from simplegmail import Gmail
from simplegmail.query import construct_query

import static.scripts.SQLServer as sqlserver_con 
# import static.scripts.SQLite as sqlite_con
from static.scripts.Gemini import Gemini


class Parser:
    def __init__(self, query_params: Dict):
        self.gmail = Gmail(client_secret_file="client_secret.json")
        self.query_params: Dict = query_params
        self.messages: List = []
        self.vacancies: Dict[str, Dict] = {}
        self.json_vacancies = "db/vacancies.json"
        self.json_last_response = "db/last_response.json"

        self.ai = Gemini()
        # self.sqlserver = sqlserver_con.Connector()
        # self.sqlite = sqlite_con.Connector()
        self.db = sqlserver_con.Connector()

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
    # FIXME - Исправить код под sql server (при необходимости)
    def write_to_db(self, vacancies: Dict[str, Dict]) -> Awaitable[bool]:
        # 1. insert into Companies, Locations
        # 2. select c_id from Companies
        # 3. use this info + json to insert into Vacancies

        # 1 -------------------
        # Companies inserts (code won't be used anymore)
        # try:
        #     companies: Set[str] = set()
        #     for date, propositions in vacancies.items():
        #         if len(propositions) == 0:
        #             continue
        #         for position, details in propositions.items():
        #             companies.add(details["company"])

        #     for company in companies:
        #         query_companies = f"""
        #             INSERT INTO Companies (Name) VALUES
        #             ('{company}');
        #         """
        #         result: bool = self.db.executeQuery(query_companies)
        #         if not result:
        #             print(f"Problem with writing: {company}")
        # except sqlite3.IntegrityError as ie:
        #     print("Companies are already inserted!")

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
        view_companies: List[Tuple] = self.db.executeQuery("SELECT * FROM Companies")["sqlite"]
        companies_sql: Dict[str, int] = {row[1]: row[0] for row in view_companies}

        view_locations: List[Tuple] = self.db.executeQuery("SELECT * FROM Locations")["sqlite"]
        locations_sql: Dict[str, int] = {row[1]: row[0] for row in view_locations}

        locations_sql2 = locations_sql.copy()
        locations_sql2.pop("Slovensko")
        # 3 -------------------
        query_vacancies: str = "INSERT INTO Vacancies (Position, Link, Company, Location, Date) VALUES"
        values: List[str] = []

        for date, propositions in vacancies.items():
            if len(propositions) == 0:
                continue
            for position, details in propositions.items():

                location_id = next(
                    (id for city, id in locations_sql2.items() if city in details["location"]),
                    locations_sql["Slovensko"]
                )

                company = details['company']
                company_id: int = companies_sql.get(company, -1)
                if company_id == -1:
                    result: bool = self.db.executeQuery(f"""
                        INSERT INTO Companies (Name) VALUES
                        ('{details['company']}');
                    """)
                    if result:
                        company_id = self.db.executeQuery(
                            f"SELECT C_id FROM Companies WHERE Name = '{details['company']}'")[0]["C_id"]
                values.append(f"('{position}', '{details['link']}', {company_id}, {location_id}, '{date}');")
        for value in values:
            try:
                query: str = f"{query_vacancies} {value}"
                result: bool = self.db.executeQuery(query)
                if not result:
                    print("Problem with writing this vacancy: ", value)
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
            self.write_to_json(unique_vacancies, self.json_vacancies)

        return unique_vacancies

    def send_request(self, v_id: int, link: str, timeout: float = 2) -> Dict[str, str | bool]:
        page: requests.Request = requests.get(link, timeout=timeout)
        soup = BeautifulSoup(page.content, 'html.parser')

        haveApplied: bool = soup.find(
            text=re.compile("Na túto pracovnú ponuku ste reagovali poslaním životopisu")
        ) is not None

        isExpired: bool = soup.find(
            text=re.compile("spoločnosť ponúkajúca danú pracovnú pozíciu ukončila")
        ) is not None

        job_panel = soup.find("div", attrs={"class": "panel-body"})
        job_panel_info: str = (
            "\n".join([line.strip() for line in job_panel.get_text().splitlines() if line.strip()])
            if job_panel else "No information found"
        )

        job_info = soup.find("div", attrs={"class": "details", "itemprop": "description"})
        job_info_text: str = job_info.get_text(separator="\n").strip() if job_info else "No information found"

        response: Dict = {
            "v_id": v_id,
            "header": job_panel_info,
            "details": job_info_text,
            "applied": haveApplied,
            "expired": isExpired
        }
        self.write_to_json(response, self.json_last_response)
        return response

    # "replace" parameter replaces only vacancies
    def read_from_json(self, json_file: str, replace: bool = False) -> Dict[str, Dict]:
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            if replace and json_file == self.json_vacancies:
                self.vacancies = data
            return data

    def write_to_json(self, data: Dict[str, Dict | str | bool], json_file: str) -> None: 
        with open(json_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
