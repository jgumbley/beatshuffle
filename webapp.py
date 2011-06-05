from functools import wraps
from flask import Flask
from flask import render_template
from flask import jsonify
from flask import redirect
from flask import session
from flask import url_for
from flask import request
from flask import flash
from flask import g
from persist import db, Mix, Tag
from flaskext.oauth import OAuth

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# sqlalchemy config:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tnz_layer:c0ns0le@localhost:5432/tnz'
db.init_app(app)

# DAO module level functions
def get_tn_by_hash(tn_hash, db):
    """This is a module level function, akin to a DAO
    """
    return db.session.query(Mix).filter(Mix.hash==tn_hash).first()

def get_all_tnz(db):
    """Returns all mixed or the empty list
    """
    return db.session.query(Mix).all()

def get_all_tags(db):
    return db.session.query(Tag).all()

def get_tag_by_name(db, tag):
    return db.session.query(Tag).filter(Tag.name==tag).first()

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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('twitter_user') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

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
    """all - will likely become stats
    """
    tnz = get_all_tnz(db)
    return render_template('index.html', tnzs=tnz)

@app.route("/")
def root():
    return redirect("/shuffle")

@app.route("/shuffle")
def genres():
    i = get_all_tags(db)
    return render_template('shuffle.html', items=i)

@app.route("/about")
def about():
    return render_template('about.html' )

@app.route("/player/<tn_hash>/")
def player(tn_hash):
    song = get_tn_by_hash(tn_hash, db)
    return render_template('player.html', tn=tn_hash, song=song)

@app.route("/retag/<tn_hash>/")
@login_required
def retag(tn_hash):
    song = get_tn_by_hash(tn_hash, db)
    u = session['twitter_user']
    return render_template('retag.html', song=song, user=u)

@app.route("/tag/<tag>/")
def tag(tag):
    t = get_tag_by_name(db, hydrate_filter(tag))
    return render_template('index.html', name=t.name, tnzs=t.tnz)

@app.route("/rmtag/<tn_hash>/<tag>/")
@login_required
def rmtag(tn_hash, tag):
    song = get_tn_by_hash(tn_hash, db)
    l = []
    for gag in song.tags:
        l.append(gag.name)
    u = session['twitter_user']
    #    return redirect(request.referrer)
    return jsonify(song=song.hash, currtags=l, tag_to_rm=hydrate_filter(tag), as_user=u)

@app.route("/addtag/<tn_hash>/")
@login_required
def addtag(tn_hash):
    u = session['twitter_user']
    song = get_tn_by_hash(tn_hash, db)
    l = []
    for tag in song.tags:
        l.append(tag.name)
    to_add = request.args['tags']
    song.add_tag(to_add)
    h = []
    for rag in song.tags:
        h.append(rag.name)
    db.session.merge(song)
    db.session.commit()
    return redirect(request.referrer)
    #return jsonify(song=song.hash, currtags=l, newtags=h, tag_to_add=to_add, as_user=u)

from flask import jsonify

# api methods
@app.route("/api/tags/")
def list_tags():
    list_of_tags = db.session.query(Tag.name).all()
    ret = [] 
    for item in list_of_tags:
        row = {}
        row['value'] = item[0]
        ret.append(row)
    return jsonify(ret)

# url manipulation
@app.template_filter('flatten')
def flatten_filter(s):
    return s.replace(" ", "_")

def hydrate_filter(s):
    return s.replace("_", " ")

# entry point
if __name__ == "__main__":
    app.debug = True
    app.run(host="172.16.26.33", port=80)

