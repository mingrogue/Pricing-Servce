import functools
from typing import Callable
from flask import session, url_for, flash, redirect, current_app


def requires_login(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('email'):
            a = session.get('email')
            print(a)
            flash('you need to be logged in to access this page', 'danger')
            redirect(url_for('users.login_user'))
        return f(*args, **kwargs)
    return decorated_function


def requires_admin(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('email') != current_app.config.get('ADMIN', ''):
            flash('You need to be an administrator to access this page', 'danger')
            return redirect(url_for('users.login_user'))
        return f(*args, **kwargs)
    return decorated_function
