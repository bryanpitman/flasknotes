"""flask app for Notes application"""

from flask import Flask, redirect, render_template, request, flash, session
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterForm, LoginForm

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
def register_form():
    """Register user: produce form & handle form submission."""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username = username,
                      password = password,
                      first_name = first_name,
                      last_name = last_name,
                      email = email)

        db.session.add(new_user)
        db.session.commit()

        session["user_id"]= new_user.id

        flash(f"Added {username}")
        return redirect("/secret")

    else:
        return render_template("register.html", form = form)

@app.route("/login", methods=["GET", "POST"])
def login_form():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(username, password)

        if user:
            session["user_id"] = user.id  # keep logged in
            return redirect("/secret")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)

@app.get("/secret")
def secret():

        return render_template("secret.html")