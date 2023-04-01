from pprint import pprint
from flask import Flask, render_template, url_for, request, redirect
from flask_login import login_user, login_required, logout_user, UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = "SECRET_KEY"
db = SQLAlchemy(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(id=user_id).first()


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    psw = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())

    pr = db.relationship('Profiles', backref='users', uselist=False)

    # def __repr__(self):
    #     return f'<users self.id>'


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    old = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))



@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        psw = request.form.get('psw')

        if email and psw:
            user = Users.query.filter_by(email=email).first()

            if user and check_password_hash(user.psw, psw):
                login_user(user)
                return redirect(url_for('index'))

            else:
                return "неправельний пароль або пошта"
        else:
            return 'будь ласка введіть правильний пароль'
    else:
        return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            hash = generate_password_hash(request.form['psw'])
            p = Profiles(name=request.form['name'], old=request.form['old'], city=request.form['city'])
            u = Users(email=request.form['email'], psw=hash, pr=p)
            
            db.session.add(p)
            db.session.add(u)
            db.session.flush()

            db.session.commit()

        except:
            db.session.rollback()
            print("помилка")

    return render_template("register.html")


@app.route('/profile')
@login_required
def profile():
    info = []
    try:
        info = Users.query.all()
        
        # Uncomment to see true magic)
        # [ pprint(x.pr.__dict__) for x in info ]
    except:
        print("помилка при читанні")
    return render_template("profile.html", list=info)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))


if __name__ == "__main__":
    app.run(debug=True)
