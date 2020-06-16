from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, current_user, login_user, login_required, logout_user

import config
from models import User
from wtform_fields import *


app = Flask(__name__)
app.secret_key = 'aaaaaaaaaaaaaaa'

app.config['SQLALCHEMY_DATABASE_URI'] = config.postgres_url

db = SQLAlchemy(app)

login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/", methods=['GET', 'POST'])
def index():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        hashed_pswd = pbkdf2_sha256.hash(password)

        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        if current_user.is_authenticated:
            return redirect(url_for('chat'))
    return render_template("login.html", form=login_form)


@app.route("/chat", methods=['GET', 'POST'])
def chat():
    if not current_user.is_authenticated:
        return "Please login"
    return "Chat with me"


@app.route("/logout", methods=['GET'])
def logout():
    logout_user()
    return "Logout user"



if __name__ == "__main__":
    app.run(debug=True)
