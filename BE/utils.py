import os, io, jwt, uuid
import pymysql
import time
import datetime

from functools    import wraps
from flask        import request, jsonify, g

from config import SECRET_KEY, ALGORITHM
from db_connector import connect_db
from model.account_dao import AccountDao


def login_validator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        access_token = request.headers.get('AUTHORIZATION', None)
        if not access_token:
            return jsonify({'MESSAGE': 'invalid_token'}), 401
        try:
            payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            account_id = payload['account_id']
            connection = connect_db()
            account_dao = AccountDao()
            account = account_dao.account_identifier(account_id, connection)
            if not account:
                return jsonify({'MESSAGE': 'account_nonexistant'}), 404
            if account['is_active'] == 0:
                return jsonify({'MESSAGE': 'account_not_active'}), 400
            g.token_info = {
                'account_id'      : account_id,
                'account_type_id' : account['account_type_id'],
                'seller_id'       : account['seller_id']}
            return func(*args, **kwargs)
        except jwt.InvalidTokenError:
            return jsonify({'MESSAGE': 'invalid_token'}), 401

    return wrapper

