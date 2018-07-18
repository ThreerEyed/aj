from flask import session, jsonify

import functools
from utils import statucode


def is_login(func):
    @functools.wraps(func)
    def check_login(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id:
            return func(*args, **kwargs)
        else:
            return jsonify(statucode.USER_NOT_LOGIN)
    return check_login
