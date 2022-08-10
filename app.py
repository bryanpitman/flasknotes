"""flask app for Notes application"""

from flask import Flask, redirect, render_template, request, flash, session
from models import db, connect_db, User, Note
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterForm, LoginForm, CSRFProtectForm, AddNoteForm

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


@app.route('/register', methods=['GET', 'POST'])
def register_form():
    """Register user: produce form & handle form submission."""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username=username,
                                 password=password,
                                 first_name=first_name,
                                 last_name=last_name,
                                 email=email)

        db.session.add(new_user)
        db.session.commit()

        session["username"] = new_user.username

        flash(f"Added {new_user.username}")
        return redirect(f"/users/{new_user.username}")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_form():
    """Produce login form or handle login."""

    # if logged in redirect to the user details page
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(username, password)

        if user:
            # keep logged in and stores a dictonary?
            # change to username below
            session["username"] = user.username  # {"user_id": 1}
            return redirect(f"/users/{username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)


@app.get("/users/<username>")
def user_details(username):
    """Check if user is logged in and Show user details"""

    if "username" not in session or session["username"] != username:
        flash("You must be logged in to view!")
        return redirect("/login")

    user = User.query.filter_by(username=username).one_or_none()
    form = CSRFProtectForm()

    return render_template("user_details.html", user=user, form=form)


@app.post("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        # Remove "user_id" if present, but no errors if it wasn't
        session.pop("username", None)

    return redirect("/")


@app.get("/users/<username>")
def user_details_notes(username):
    """Check if user is logged in and show user detail and notes"""

    if "username" not in session or session["username"] != username:
        flash("You must be logged in to view!")
        return redirect("/login")

    user = User.query.filter_by(username=username).one_or_none()
    notes = Note.query.filter_by(owner=user.id).all()
    form = CSRFProtectForm()

    return render_template("user_details.html", notes=notes, form=form)


@app.post("/users/<username>/delete")
def delete_user(username):
    """delete user"""

    if "username" not in session or session["username"] != username:
        flash("You must be logged in to view!")
        return redirect("/login")

    form = CSRFProtectForm()

    if form.validate_on_submit():
        # clear session
        session.pop("username", None)  # pop first or last? doesn't matter

        # select user
        # select all user posts
        user = User.query.filter_by(username=username).one_or_none()
        notes = user.notes

        # delete notes then delete user
        db.session.delete(*notes)
        db.session.commit()

        db.session.delete(user)
        db.session.commit()

        return redirect("/")


@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def add_note_form(username):
    """Add note for user form"""

    if "username" not in session:
        return redirect("/login")

    form = AddNoteForm()
    user = User.query.filter_by(username=username).one_or_none()

    if form.validate_on_submit():

        title = form.title.data
        content = form.content.data

        note = Note(title=title, content=content, owner=user.id)

        db.session.add(note)
        db.session.commit()

        return redirect("/users/<username>")

    else:
        return render_template("add_note.html", form=form, user=user)
