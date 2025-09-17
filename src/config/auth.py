from functools import wraps
from flask import request

def require_api_key(expected_key):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = request.headers.get("api-key")
            if key != expected_key:
                return {"error": "Nao Autorizado"}, 401
            return func(*args, **kwargs)
        return wrapper
    return decorator