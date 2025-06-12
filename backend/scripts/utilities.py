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
            
            if isinstance(response, Response):
                return response
            
            elif isinstance(response, tuple) and len(response) == 2:
                data, status = response
                
                if isinstance(data, dict):
                    data['_meta'] = {'handler': func.__name__}
                    return jsonify(data), status
                
                return response
            
            return jsonify(response)
            
        except Exception as e:
            error_data = {
                **getattr(e, 'error_data', {}),
                "location": f"{func.__module__}.{func.__name__}",
                "type": type(e).__name__,
                "error": str(e)
            }
            return jsonify(error_data), 500
    return wrapper

def handle_db_connection(func: Callable):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            self.conn.connect()
            result = func(self, *args, **kwargs)
            return result
        except Exception as e:
            return {f"error ({func.__name__})": str(e)}
    return wrapper

