from functools import wraps
from typing import Callable
from flask import jsonify

def specify_error(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_data = {
                "error": str(e),
                "location": f"file: {__name__}, func: {func.__name__}",
                "type": type(e).__name__
            }
            return jsonify(error_data), 500
    return wrapper