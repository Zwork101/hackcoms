from crypt import methods
from db import User, create_user

from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import Form, BooleanField, PasswordField, StringField, validators

class RegistrationForm(FlaskForm):
    username     = StringField('Username', [validators.Length(min=4, max=25)])
    first_name   = StringField('First Name', [validators.Length(min=1, max=25)])
    last_name    = StringField('Password', [validators.Length(min=1, max=25)])
    hearing_impaired = BooleanField("Hearing Impaired", default=False)
    require_interpreter = BooleanField("Require Interpreter", default=False)
    password     = PasswordField("Password", [validators.Length(min=6, max=25)])
    accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])

login_manager = LoginManager()
auth = Blueprint("auth", __name__)

@login_manager.user_loader
def load_user(user_id: int) -> User:
    return User.query.get(user_id)

@auth.route("/register", methods=["GET", "POST"])
def register_user():
    form = RegistrationForm()

    if form.validate_on_submit():

        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash("Username already in use, have you tried: 'cheese2'?")
            return redirect(url_for('auth.signup'))

        user = create_user(
            request.form.get("username"),
            request.form.get("password"),
            request.form.get("first_name"),
            request.form.get("last_name"),
            request.form.get("hearing_impaired"),
            request.form.get("require_interpreter")
        )

        login_user(User)

        return redirect(url_for("home.index"))

    return render_template("auth/register.html", form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home.index"))