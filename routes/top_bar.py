from flask import Blueprint, render_template, jsonify, redirect, flash
from services.parser_service import parser_service
from static.scripts.utilities import handle_errors

bp = Blueprint("main", __name__, url_prefix="/bar")

@bp.route("/newest")
@handle_errors
def load_newest_vacancies():
    parser_service.load_newest_vacancies()
    flash("Vacancies are now up to date!")
    return redirect("/")
    
@bp.route("/matching")
@handle_errors
def matching():
    pass

@bp.route("/filters/<string:name>")
@handle_errors
def apply_filters(filter_name: str):
    pass