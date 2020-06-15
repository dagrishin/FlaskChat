from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from models import User
from wtform_fields import *


app = Flask(__name__)
app.secret_key = 'aaaaaaaaaaaaaaa'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgres://vvskxyyxkbxltd:c5b7223c225437f0402733c08a2cb3a4563986b0afbf5349b4ee3c0851717a09@ec2-54-247-118-139.eu-west-1.compute.amazonaws.com:5432/dau8ght2s2j958'

db = SQLAlchemy(app)

@app.route("/", methods=['GET', 'POST'])
def index():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        user_object = User.query.filter_by(username=username).first()
        if user_object:
            return "Someone else has taken this username!"
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "Inserted into DB!"

    return render_template("index.html", form=reg_form)

if __name__ == "__main__":
    app.run(debug=True)
