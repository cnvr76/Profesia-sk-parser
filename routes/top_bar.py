from flask import Blueprint, render_template, jsonify, redirect
from services.parser_service import parser_service
from static.scripts.utilities import handle_errors

bp = Blueprint("main", __name__, url_prefix="/bar")

@bp.route("/newest")
@handle_errors
def load_newest_vacancies():
    parser_service.load_newest_vacancies()
    return redirect("/")
    
@bp.route("/matching")
@handle_errors
def matching():
    pass

@bp.route("/filters/<string:name>")
@handle_errors
def apply_filters(name: str):
    filtered_data = parser_service.filter_vacancies(name)
    return render_template("index_redesign.html", vacancies=filtered_data), 200