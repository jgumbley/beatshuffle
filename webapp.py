from flask import Flask
from flask import render_template
from flask import jsonify
from flask import redirect
from flask import session
from flask import url_for
from flask import request
from flask import flash
from flaskext.sqlalchemy import SQLAlchemy
from persist import Mix, Tag
from flaskext.oauth import OAuth

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# sqlalchemy config:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tnz_layer:c0ns0le@localhost:5432/tnz'
db = SQLAlchemy(app)

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

@app.route('/login')
def login():
    return twitter.authorize(callback=url_for('oauth_authorized',
        next=request.args.get('next') or request.referrer or None))

@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)

# web methods:

@app.route("/all")
def index():
    tnz = db.session.query(Mix).all()
    return render_template('index.html', tnzs=tnz)

@app.route("/")
def root():
    return redirect("/shuffle")

@app.route("/shuffle")
def genres():
    i = db.session.query(Tag).all()
    return render_template('shuffle.html', items=i)

@app.route("/about")
def about():
    return render_template('about.html' )

@app.route("/player/<tn_hash>/")
def player(tn_hash):
    song = db.session.query(Mix).filter(Mix.hash==tn_hash).first()
    u = session['twitter_user']
    return render_template('player.html', tn=tn_hash, song=song, user=u)

@app.route("/tag/<tag>/")
def tag(tag):
    tagv = hydrate_filter(tag)
    #t = db.session.query(Mix).filter(Mix.tags.contains(tagv)).all()
    t = db.session.query(Tag).filter(Tag.name==tagv).first()
    return render_template('index.html', name=t.name, tnzs=t.tnz)


@app.template_filter('flatten')
def flatten_filter(s):
    return s.replace(" ", "_")

def hydrate_filter(s):
    return s.replace("_", " ")

if __name__ == "__main__":
    app.debug = True
    app.run(host="172.16.26.33", port=80)

