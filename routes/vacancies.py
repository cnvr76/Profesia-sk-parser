from flask import Blueprint, render_template, jsonify, flash
from services.parser_service import parser_service
from static.scripts.utilities import specify_error

bp = Blueprint("vacancies", __name__, url_prefix='/vacancies')

@bp.route("/<int:v_id>/details")
@specify_error
def show_details(v_id: int):
    try:
        details = parser_service.get_vacancy_details(v_id)
        return jsonify(details), 200
    except Exception as e:
        return jsonify({f"error ({__name__})": str(e)}), 500
    
@bp.route("/<int:v_id>/star")
@specify_error
def star_vacancy(v_id: int):
    try:
        result = parser_service.star_vacancy(v_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({f"error ({__name__})": str(e)}), 500
    
@bp.route("/<int:v_id>/delete", methods=["DELETE"])
@specify_error
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