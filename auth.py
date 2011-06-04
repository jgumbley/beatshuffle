from flaskext.oauth import OAuth
from flask import session

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

@twitter.tokengetter
def get_twitter_token():
    return session.get('twitter_token')



