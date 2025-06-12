
if __name__ == '__main__':
    query_params = {
        "newer_than": (10, "day"),
        "older_than": (1, "day"),
        "sender": "support@profesia.sk"
    }
    # parser: Parser = Parser(query_params)

    # sqlite - data selection
    # data = parser.sqlite.connect().executeQuery("select * from Vacancies")
    # print(data)

    # sql server - data insertion
    # parser.sqlserver.connect()

    # for row in data:
    #     date = datetime.fromisoformat(row["Date"][:-6])  # Преобразуем в объект даты
    #     formatted_date = date.strftime('%Y-%m-%d %H:%M:%S')  # Форматируем для SQL

    #     params = (row["Position"], row["Link"], row["Company"], row["Location"], date)
    #     parser.sqlserver.executeQuery("""
    #         INSERT INTO Vacancies (Position, Link, Company, Location, Date)
    #         VALUES (?, ?, ?, ?, ?);
    #     """, params)


    # messages = parser.get_messages()
    # vacancies = parser.parse_messages(messages)
    # unique_vacancies = parser.remove_duplicates(vacancies, replace=True)
    # parser.write_to_json()

    # data = parser.read_from_json()
    # parser.write_to_db(data)

    # response = parser.send_request("https://tr.profesia.sk/lnk/EAAABoaK4O0AAcqpLBYAAL9CtXIAAAAAimgAAAAAAAj8PQBnh6LUI5fGC3CwRaO0zxI_Rz0XOQAIUkc/3/Hhk2PDK4_S8PZisbF3Z77A/aHR0cHM6Ly93d3cucHJvZmVzaWEuc2svcHJhY2EvcGV0aXQtcHJlc3MvTzQ5NzkwMTI_cnVsb2dpbj02ZmJhNTBhODM5NWNmMDRmOTgxNGNiMGJiNDc4NmRiNSZzdWdnZXN0X2lkPTM3M2I1NjMyLTZmOTQtNGZjNy05MDgxLThiOGQ1ZjExOWYzZCZyaWQ9ZGFlMmFhYzIzNTIxZDZkYiZydW49YWFjZSZ1dG1fbWVkaXVtPW1haWwmdXRtX3NvdXJjZT0xMDE0MyZ1dG1fY29udGVudD1vdGhlciZ1dG1fY2FtcGFpZ249MTAxNDMmdXRtX3Rlcm09MjAyNS0wMS0xNQ")
    #
    # prompt = parser.ai.make_prompt(question="Что мне нужно знать для этой вакансии (на словацком)",
    #                                context=f"Header of the vacancy: {response['header']}\nBody{response['details']}")
    # answer = parser.ai.ask(prompt)

    # answer = parser.ai.load_json_answer()
    # pprint(answer)
