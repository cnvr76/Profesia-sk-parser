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
        data = parser.db.connect().all()
        parser.db.close()
        return render_template("index_redesign.html", vacancies=data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/<v_id>/details")
def show_details(v_id):
    try:
        parser.db.connect()

        # data: Dict = parser.db.executeQuery("SELECT Link FROM Vacancies WHERE V_id = ?", (v_id))[0]
        
        # response: Dict = parser.send_request(link=data["Link"])
        
        # prompt: str = parser.ai.make_prompt(
        #     question="Что мне нужно знать для этой вакансии (на словацком)",
        #     context=f"Header of the vacancy: {response['header']}\nBody: {response['details']}"
        # )
        
        # answer = parser.ai.ask(prompt)
        answer = parser.ai.load_json_answer()
        response = parser.read_from_json(parser.json_last_response)

        try:
            salary: int = int(''.join(re.findall(r"\d+", answer["salary"])))
            query: str = f"INSERT INTO Vacancies(Salary, Description, haveApplied, hasExpired) VALUES ({salary}, '{answer['summary']}', {int(response['applied'])}, {int(response['expired'])});"
            result: bool = parser.db.executeQuery(query)
        except Exception as e:
            flash(message=f"Problem with writing vacancy to db: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
        for knowledge in answer["knowledge"]:
            try: 
                query: str = f"INSERT INTO Knowledges(V_id, Field, Description) VALUES ({v_id}, '{knowledge['name']}', '{knowledge['description']}')"
                parser.db.executeQuery(query)
            except Exception as e:
                flash(message=f"Problem with writing knowledges to db: {str(e)}")
                return jsonify({"error": str(e)}), 500

        details: Dict = parser.db.executeQuery("""
            SELECT v.Position, v.Link, v.Company, v.Location, v.Salary, v.haveApplied, v.hasExpired,
                   k.Field, k.Description
            FROM Vacancies v
            JOIN Knowledges k ON k.V_id = v.V_id
            WHERE v.V_id = ?
        """, (v_id))[0]
        
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
