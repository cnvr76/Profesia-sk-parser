from flask import Blueprint, render_template, jsonify
from services.parser_service import parser_service

bp = Blueprint("main", __name__)

@bp.route("/", methods=['GET', 'POST'])
def home():
    try:
        parser_service.conn.connect()
        data = parser_service.conn.all()
        parser_service.conn.close()
        return render_template("index_redesign.html", vacancies=data), 200
    except Exception as e:
        return jsonify({f"error ({__name__})": str(e)}), 500