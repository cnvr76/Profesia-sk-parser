from flask import Blueprint, render_template, jsonify, flash
from services.parser_service import parser_service

bp = Blueprint("vacancies", __name__, url_prefix='/vacancies')

@bp.route("/<int:v_id>/details")
def show_details(v_id: int):
    try:
        details = parser_service.get_vacancy_details(v_id)
        return jsonify(details), 200
    except Exception as e:
        return jsonify({f"error ({__name__})": str(e)}), 500