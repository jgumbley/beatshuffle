from flask import Flask
from flask import render_template
from flaskext.sqlalchemy import SQLAlchemy
from persist import Mix

app = Flask(__name__)

# sqlalchemy config:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tnz_layer:c0ns0le@localhost:5432/tnz'
db = SQLAlchemy(app)

@app.route("/")
def index():
    tnz = db.session.query(Mix).all()
    return render_template('index.html', tnzs=tnz)

@app.route("/player/<tn_hash>/")
def player(tn_hash):
    return render_template('player.html', tn=tn_hash)

if __name__ == "__main__":
    app.debug = False
    app.run(host="172.16.26.33")

