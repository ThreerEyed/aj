from functools import wraps

from flask import session, redirect, url_for


def is_login(func):
    @wraps(func)
    def check_login(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('user.login'))
        else:
            return func(*args, **kwargs)
    return check_login
