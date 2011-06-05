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

@twitter.tokengetter
def get_twitter_token():
    return session.get('twitter_token')

def do_login():
    return twitter.authorize(callback=url_for('oauth_authorized',
        next=request.args.get('next') or request.referrer or None))

def do_oauth_callback(resp):
    """ this is the call back after login
    """
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']
    return redirect(next_url)

