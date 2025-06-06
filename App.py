from static.scripts.Parser import Parser
from flask import Flask, jsonify, render_template, flash
from typing import Dict, Tuple, List
import os
import dotenv

# TODO - при сохранении с общего -> обновляется и в деталях, и в общем
# при сохранении с деталей -> обновляется у обоих, но потом резко в исходное

# TODO - удаление выдает ошибку джсона, но все равно вакансия удаляется при обновлении

dotenv.load_dotenv()

app = Flask(__name__, template_folder="./templates", static_folder="./static")
app.secret_key = os.getenv("FLASK_SECRET_KEY") 

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
        return render_template("index_redesign.html", vacancies=data["view"]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/<int:v_id>/details")
def show_details(v_id):
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
                WHERE V_id = ?
            """, (v_id,))["view"][0]
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
                parser.db.update_vacancy_details(v_id, answer, response)
            except Exception as e:
                flash(message=f"Problem with writing vacancy to db: {str(e)}")
                return jsonify({"error": str(e)}), 404
        
        # Writing info to db (table Knowledges)
        knowledgesExist: bool = len(parser.db.executeQuery("SELECT * FROM Knowledges WHERE V_id = ?", (v_id))["sqlite"]) > 0
        if not knowledgesExist:
            for knowledge in answer["knowledge"]:
                try:
                    parser.db.executeQuery("INSERT INTO Knowledges(V_id, Field, Description) VALUES (?, ?, ?)", 
                                        (v_id, knowledge['name'], knowledge['description']))
                except Exception as e:
                    flash(message=f"Problem with writing knowledges to db: {str(e)}")
                    return jsonify({"error": str(e)}), 404
                
        frameworksExist: bool = len(parser.db.executeQuery("SELECT * FROM Frameworks WHERE V_id = ?", (v_id))["sqlite"]) > 0
        if not frameworksExist:
            for framework in answer["frameworks"]:
                try: 
                    parser.db.executeQuery("INSERT INTO Frameworks(V_id, Name) VALUES (?, ?)", (v_id, framework))
                except Exception as e:
                    flash(message=f"Problem with writing frameworks to db: {str(e)}")
                    return jsonify({"error": str(e)}), 404

        # Final details of the vacancy
        details: Dict = parser.db.executeQuery("""
            SELECT v.V_id, v.Position, v.Link, c.Name as 'Company', l.City as 'Location',
                    v.Salary, v.haveApplied, v.hasExpired, s.S_id as 'isStarred'
            FROM Vacancies v
            JOIN Companies c ON c.C_id = v.Company
            JOIN Locations l ON l.L_id = v.Location
            LEFT JOIN Starred s ON v.V_id = s.V_id                                               
            WHERE v.V_id = ?
        """, (v_id))["view"][0]

        knowledges: Dict = parser.db.executeQuery("""
            SELECT Field, Description
            FROM Knowledges
            WHERE V_id = ?
        """, (v_id))["view"]

        frameworks: Dict = parser.db.executeQuery("""
            SELECT Name
            FROM Frameworks
            WHERE V_id = ?
        """, (v_id))["view"]

        details["Knowledges"] = knowledges
        details["Frameworks"] = frameworks
        
        return jsonify(details), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        parser.db.close()


@app.route("/<int:v_id>/delete", methods=["GET", "POST"])
def delete_vacancy(v_id):
    try:
        parser.db.connect()
        # success: bool = parser.db.executeQuery("DELETE FROM Vacancies WHERE v_id = ?", (v_id,))
        success: bool = True
        if success:
            return jsonify({"executed": success}), 204
        else:
            return jsonify({"error": "Not deleted"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/<int:v_id>/save", methods=["GET", "POST"])
def save_vacancy(v_id):
    try:
        parser.db.connect()
        parser.db.connect()

        result: Dict[str, List] = parser.db.executeQuery("SELECT V_id FROM Starred WHERE V_id = ?", (v_id,))
        exists: bool = bool(result.get("view"))

        if exists:
            executed: bool = parser.db.executeQuery("DELETE FROM Starred WHERE V_id = ?", (v_id,))
            isStarred: bool = False 
            flash("Vacancy removed from starred")
        else:
            executed: bool = parser.db.executeQuery("INSERT INTO Starred(V_id) VALUES(?)", (v_id,))
            isStarred: bool = True
            flash("Vacancy added to starred")

        return jsonify({"executed": executed, "starred": isStarred}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500



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
