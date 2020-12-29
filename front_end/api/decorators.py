from functools import wraps
from flask import session, redirect, url_for


#used as a decorator, under the route decorator, check if user is logged in
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        #if logged_in value not exist or false, then user is not logged in
        try:
            if not session['logged_in']:
                return redirect(url_for('auth.access_denied'))
        except:
            return redirect(url_for('auth.access_denied'))

        return func(*args, **kwargs)

    return decorated_function