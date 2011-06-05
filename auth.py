from functools import wraps
from flaskext.oauth import OAuth
from flask import session
from flask import redirect
from flask import url_for 
from flask import request

# OAuth config:
oauth = OAuth()

twitter = oauth.remote_app('twitter',
    base_url='http://api.twitter.com/1/',
    request_token_url='http://api.twitter.com/oauth/request_token',
    access_token_url='http://api.twitter.com/oauth/access_token',
    authorize_url='http://api.twitter.com/oauth/authenticate',
    consumer_key='aMCIQI4nO4V1FDuGps8nRw',
    consumer_secret='EI7t8s8nefbqlpx0xcKgbitiHwn3ydpTGCWIWUsgug'
)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('twitter_user') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function



