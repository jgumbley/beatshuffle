from flask import Flask
from flask import render_template
from flask import jsonify
from flask import redirect
from flask import session
from flask import url_for
from flask import request
from flask import flash

from auth import twitter, login_required, do_login, do_oauth_callback

from persist import get_tn_by_hash, get_all_tnz, get_all_tags, get_tag_by_name
from persist import db, Mix, Tag

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# sqlalchemy config:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tnz_layer:c0ns0le@localhost:5432/tnz'
db.init_app(app)

# Auth related web - delegate into auth module 
@app.route('/login')
def login():
    return do_login()

@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    return do_oauth_callback(resp)

# web methods:

@app.route("/all")
def index():
    """all - will likely become stats
    """
    tnz = get_all_tnz()
    return render_template('index.html', tnzs=tnz)

@app.route("/")
def root():
    return redirect("/shuffle")

@app.route("/shuffle")
def shuffle():
    i = get_all_tags()
    return render_template('shuffle.html', items=i)

@app.route("/about")
def about():
    return render_template('about.html' )

@app.route("/player/<tn_hash>/")
def player(tn_hash):
    song = get_tn_by_hash(tn_hash)
    return render_template('player.html', tn=tn_hash, song=song)

@app.route("/retag/<tn_hash>/")
@login_required
def retag(tn_hash):
    song = get_tn_by_hash(tn_hash)
    u = session['twitter_user']
    return render_template('retag.html', song=song, user=u)

@app.route("/tag/<tag>/")
def tag(tag):
    t = get_tag_by_name(hydrate_filter(tag))
    return render_template('index.html', name=t.name, tnzs=t.tnz)


def rm_tag_from_song(user, song_hash, tag):
    song = get_tn_by_hash(song_hash)
    if len(song.tags) == 1:
        flash("must have at least one tag")
    else:
        new_tags=[]
        for t in song.tags:
            if t.name in tag:
                flash(t.name + " removed")
            else:
                new_tags.append(t)
        song.tags = new_tags
        db.session.merge(song)
        db.session.commit()


@app.route("/rmtag/<tn_hash>/<tag>/")
@login_required
def rmtag(tn_hash, tag):
    user = session['twitter_user']
    rm_tag_from_song(user, tn_hash, tag)
    return redirect(request.referrer)

def add_tag_to_song(user, song_hash, tag):
    song = get_tn_by_hash(song_hash)
    song.add_tag(tag)
    db.session.merge(song)
    db.session.commit()

@app.route("/addtag/<tn_hash>/")
@login_required
def addtag(tn_hash):
    user = session['twitter_user']
    to_add = request.args['tags']
    add_tag_to_song(user, tn_hash, to_add)
    return redirect(request.referrer)

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

