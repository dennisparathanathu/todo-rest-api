from flask import jsonify, request
from functools import wraps
import jwt
import os
from .models import UserModel


class Auth:
    @staticmethod
    def token_required(f):

        @wraps(f)
        def decorator(*args, **kwargs):

            token = None

            if 'x-access-tokens' in request.headers:
                token = request.headers['x-access-tokens']

            if not token:
                return jsonify({'message': 'a valid token is missing'})

            try:
                data = jwt.decode(token, os.getenv('JWT_SECRET_KEY'))
                current_user = UserModel.query.filter_by(id=data['user_id']).first()
            except:
                return jsonify({'message': 'token is invalid'})

            return f(current_user, *args, **kwargs)

        return decorator
