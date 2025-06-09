from flask import Blueprint, render_template, jsonify
from services.parser_service import parser_service
from static.scripts.utilities import handle_errors

bp = Blueprint("home", __name__)

@bp.route("/", methods=['GET', 'POST'])
@handle_errors
def home():
    data = parser_service.load_all_data()
    return render_template("index_redesign.html", vacancies=data), 200