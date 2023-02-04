from functools import wraps
from flask import request, jsonify, make_response


def jwt_token_middleware(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        authTokenInfo = request.headers.get('Authorization')

        if authTokenInfo is None:
            return make_response(jsonify({"message": "Unauthorized"}), 401)

        authToken = authTokenInfo.split(' ')[1]

        if authToken != "mock_token_aJJSVxxx":
            return make_response(jsonify({"message": "Unauthorized"}), 401)

        print('=> jwt_token_middleware Middleware pass')
        return f(*args, **kwargs)

    return wrap
