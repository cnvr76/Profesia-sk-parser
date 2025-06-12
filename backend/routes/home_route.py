from flask import Blueprint, render_template, jsonify
from services.parser_service import parser_service
from scripts.utilities import handle_errors
from flask_cors import cross_origin
import time

bp = Blueprint("home", __name__)

@bp.route("/", methods=['GET', 'POST'])
@cross_origin()
@handle_errors
def home():
    data = parser_service.load_all_data() # Возвращает список со словарями
    return jsonify(data) # Скорее всего уже это переделывает в словарь свой 
    return render_template("index_redesign.html", vacancies=data), 200