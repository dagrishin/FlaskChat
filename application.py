from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256

import config
from models import User
from wtform_fields import *


app = Flask(__name__)
app.secret_key = 'aaaaaaaaaaaaaaa'

app.config['SQLALCHEMY_DATABASE_URI'] = config.postgres_url

db = SQLAlchemy(app)


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
        return "Logged in, finally!"

    return render_template("login.html", form=login_form)


if __name__ == "__main__":
    app.run(debug=True)
