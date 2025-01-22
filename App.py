from public.scripts.Parser import Parser
from flask import Flask, jsonify, render_template

app = Flask(__name__, template_folder="./views", static_folder="./public")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/getAll")
def get_all():
    try:
        query_params = {
            "newer_than": (10, "day"),
            "older_than": (1, "day"),
            "sender": "support@profesia.sk"
        }
        parser = Parser(query_params)
        data = parser.db.executeQuery("SELECT * FROM Companies")
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
