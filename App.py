from static.scripts.Parser import Parser
from flask import Flask, jsonify, render_template
from datetime import datetime

app = Flask(__name__, template_folder="./templates", static_folder="./static")

query_params = {
    "newer_than": (5, "day"),
    "older_than": (1, "day"),
    "sender": "support@profesia.sk"
}
parser = Parser(query_params)

@app.route("/", methods=['GET'])
def home():
    try:
        data = parser.db.connect().all()
        return render_template("index_redesign.html", vacancies=data)
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
