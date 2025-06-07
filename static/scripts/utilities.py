from functools import wraps
from typing import Callable
from flask import jsonify

from functools import wraps
from typing import Callable, Union, Tuple, Dict
from flask import jsonify, Response

def handle_errors(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            
            # Если функция вернула готовый Response (например, jsonify) — ничего не меняем
            if isinstance(response, Response):
                return response
            
            # Если функция вернула кортеж (data, status)
            elif isinstance(response, tuple) and len(response) == 2:
                data, status = response
                
                # Если data — словарь, добавляем _meta
                if isinstance(data, dict):
                    data['_meta'] = {'handler': func.__name__}
                    return jsonify(data), status
                
                # Иначе просто возвращаем как есть
                return response
            
            # Во всех остальных случаях — оборачиваем в jsonify
            return jsonify(response)
            
        except Exception as e:
            error_data = {
                **getattr(e, 'error_data', {}),
                "location": f"{func.__module__}.{func.__name__}",
                "type": type(e).__name__,
                "error": str(e)  # Добавляем текст ошибки для отладки
            }
            return jsonify(error_data), 500
    return wrapper