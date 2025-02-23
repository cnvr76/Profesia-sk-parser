from static.scripts.Parser import Parser
from flask import Flask, jsonify, render_template, flash
from datetime import datetime
from typing import Dict, Tuple, List
import re

app = Flask(__name__, template_folder="./templates", static_folder="./static")

query_params = {
    "newer_than": (5, "day"),
    "older_than": (1, "day"),
    "sender": "support@profesia.sk"
}
parser = Parser(query_params)

@app.route("/", methods=['GET', 'POST'])
def home():
    try:
        parser.db.connect()
        data = parser.db.all()
        parser.db.close()
        return render_template("index_redesign.html", vacancies=data["view"])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/<v_id>/details")
def show_details(v_id):
    v_id = int(v_id)
    try:
        parser.db.connect()
        
        data: Dict = parser.db.executeQuery("SELECT * FROM Vacancies WHERE V_id = ?", (v_id))["view"][0]

        # Getting info for the vacation
        last_response: Dict = parser.read_from_json(parser.json_last_response)
        response = last_response
        detailsExist: bool = data["Salary"] != None
        answer: Dict = {}

        if v_id == last_response["v_id"]:
            answer = parser.ai.load_json_answer()
        # If the row has any type of the missing data
        elif detailsExist:
            answer = parser.db.executeQuery("""
                SELECT Salary as 'salary', Description as 'summary', 
                                            haveApplied as 'applied', hasExpired as 'expired' 
                FROM Vacancies
            """)["view"][0]
        else:
            response = parser.send_request(v_id, link=data["Link"])
            prompt: str = parser.ai.make_prompt(
                question="Что мне нужно знать для этой вакансии (на словацком) + зарплату бери минимальную и одним числом",
                context=f"Header of the vacancy: {response['header']}\nBody: {response['details']}"
            )
            answer = parser.ai.ask(prompt)


        # Writing missing info to db (table Vacations)
        if not detailsExist:
            try:
                salary: int = int(''.join(re.findall(r"\d+", answer["salary"])))
                parser.db.executeQuery("""
                    UPDATE Vacancies
                    SET 
                        Salary = CASE WHEN Salary IS NULL THEN ? ELSE Salary END,
                        Description = CASE WHEN Description IS NULL THEN ? ELSE Description END,
                        haveApplied = CASE WHEN haveApplied IS NULL THEN ? ELSE haveApplied END,
                        hasExpired = CASE WHEN hasExpired IS NULL THEN ? ELSE hasExpired END
                    WHERE V_id = ?;
                """,
                (salary, answer['summary'], int(response['applied']), int(response['expired']), v_id))
            except Exception as e:
                flash(message=f"Problem with writing vacancy to db: {str(e)}")
                return jsonify({"error": str(e)}), 500
        
        # Writing info to db (table Knowledges)
        knowledgesExists: bool = len(parser.db.executeQuery("SELECT * FROM Knowledges WHERE V_id = ?", (v_id))["sqlite"]) > 0
        if not knowledgesExists:
            for knowledge in answer["knowledge"]:
                try: 
                    parser.db.executeQuery("INSERT INTO Knowledges(V_id, Field, Description) VALUES (?, ?, ?)", 
                                        (v_id, knowledge['name'], knowledge['description']))
                except Exception as e:
                    flash(message=f"Problem with writing knowledges to db: {str(e)}")
                    return jsonify({"error": str(e)}), 500

        # Final details of the vacancy
        details: Dict = parser.db.executeQuery("""
            SELECT v.Position, v.Link, c.Name as 'Company', l.City as 'Location',
                    v.Salary, v.haveApplied, v.hasExpired
            FROM Vacancies v
            JOIN Companies c ON c.C_id = v.Company
            JOIN Locations l ON l.L_id = v.Location
            WHERE v.V_id = ?
        """, (v_id))["view"][0]

        knowledges: Dict = parser.db.executeQuery("""
            SELECT Field, Description
            FROM Knowledges
            WHERE V_id = ?
        """, (v_id))["view"]

        details["Knowledges"] = knowledges
        
        return jsonify(details)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        parser.db.close()



@app.route("/test", methods=['GET'])
def test():
    try:
        # data = parser.read_from_json()
        # parser.db.connect()
        # response = parser.write_to_db(data)
        # return jsonify(response)

        # data = parser.db.connect().executeQuery("SELECT Date FROM Vacancies")
        # dates = [elem["Date"] for elem in data]
        # parsed_dates = [datetime.fromisoformat(date) for date in dates]
        return {}
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
