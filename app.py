from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    psw = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    pr = db.relationship('Profiles', backref='users', uselist=False)

    def __repr__(self):
        return f'<users self.user_id>'


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    old = db.Column(db.String(100), nullable=False)
    city = db.Column(db.DateTime, default=datetime.utcnow())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<profiles self.user_id>'


@app.route('/')
def index():
    info = []
    try:
        info = Users.query.all()
    except:
        print("помилка при читанні")
    return render_template("index.html", title="Main", list=info)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            hash = generate_password_hash(request.form['psw'])
            u = Users(email=request.form['email'], psw=hash)
            db.session.add(u)
            db.session.flush()

            p = Profiles(name=request.form['name'], old=request.form['old'], city=request.form['city'], user_id = u.id)

            db.session.add(p)
            db.session.commit()

        except:
            db.session.rollback()
            print("помилка")

    return render_template("register.html", title="register")


if __name__ == "__main__":
    app.run(debug=True)

