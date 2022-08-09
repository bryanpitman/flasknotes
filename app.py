"""flask app for Notes application"""
from flask import Flask, redirect, render_template, request
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()


@app.get('/')
def load_root_page():
    """Redirect to register page."""

    return redirect("/register")

@app.route('/register', methods = ['GET', 'POST'])
def show_register_form():
    """add a new user"""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User(username = username,
                      password = password,
                      first_name = first_name,
                      last_name = last_name,
                      email = email)
        db.session.add(new_user)
        db.session.commit()

        flash(f"Added {username}")
        return redirect("/secret")

    else:
        return render_template("register.html", form = form)