from public.scripts.Parser import Parser
from flask import Flask, jsonify, render_template

app = Flask(__name__, template_folder="./views", static_folder="./public")

query_params = {
    "newer_than": (10, "day"),
    "older_than": (1, "day"),
    "sender": "support@profesia.sk"
}
parser = Parser(query_params)

@app.route("/", methods=['GET'])
def home():
    try:
        data = parser.db.connect().all()
        # return data
        return render_template("index_redesign.html", vacancies=data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/getAll")
def get_all():
    try:
        data = parser.db.connect().executeQuery("SELECT * FROM Vacancies")
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
