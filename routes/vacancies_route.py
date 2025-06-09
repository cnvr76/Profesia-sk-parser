from flask import Blueprint, render_template, jsonify, flash
from services.parser_service import parser_service
from static.scripts.utilities import handle_errors

bp = Blueprint("vacancies", __name__, url_prefix='/vacancies')

@bp.route("/<int:v_id>/details")
@handle_errors
def show_details(v_id: int):
    details = parser_service.get_vacancy_details(v_id)
    return jsonify(details), 200
    
@bp.route("/<int:v_id>/star", methods=["POST"])
@handle_errors
def star_vacancy(v_id: int):
    result = parser_service.star_vacancy(v_id)
    return jsonify(result), 200
    
@bp.route("/<int:v_id>/delete", methods=["DELETE"])
def delete_vacancy(v_id: int):
    try:
        result = parser_service.delete_vacancy(v_id)
        return jsonify({
            "hasExecuted": result.get("executed", False),
            "isDeleted": True if result.get("executed") else False
        }), 200
    except Exception as e:
        return jsonify({
            "hasExecuted": False,
            "isDeleted": False,
            "error": str(e)
        }), 500