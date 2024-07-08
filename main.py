from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

with open('config.json', 'r') as c:
    params = json.load(c)("params")

local_server = True
app = Flask(__name__)
if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']

else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    face = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.String(20), nullable=True)


@app.route("/")
def hello():
    return 'Success!'


@app.route("/homepage", method=['GET', 'POST'])
def homepage():
    if (request.method == 'POST'):
        name = request.form.get('name')

        entry = User(name=name, datetime=datetime.now())
        db.session.add(entry)
        db.session.commit()

    return render_template('index.html')


app.run(debug=True)
