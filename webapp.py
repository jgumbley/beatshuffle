from flask import Flask
from flask import render_template
from flaskext.sqlalchemy import SQLAlchemy
from persist import Mix, Tag

app = Flask(__name__)

# sqlalchemy config:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tnz_layer:c0ns0le@localhost:5432/tnz'
db = SQLAlchemy(app)

@app.route("/all")
def index():
    tnz = db.session.query(Mix).all()
    return render_template('index.html', tnzs=tnz)

@app.route("/")
def genres():
    i = db.session.query(Tag).all()
    return render_template('cloud.html', items=i)

@app.route("/player/<tn_hash>/")
def player(tn_hash):
    return render_template('player.html', tn=tn_hash)

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

