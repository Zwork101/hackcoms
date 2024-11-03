from flask import Blueprint, abort, render_template, request
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash
from wtforms import BooleanField, PasswordField, SelectField, StringField, validators

from db import Role, User, list_roles, save_db

profile = Blueprint('profile', __name__)

class EditProfileForm(FlaskForm):
	username            = StringField('Username', [validators.Length(min=4, max=25)])
	first_name          = StringField('First Name', [validators.Length(min=1, max=25)])
	last_name           = StringField('Password', [validators.Length(min=1, max=25)])
	hearing_impaired    = BooleanField("Hearing Impaired", default=False)
	require_interpreter = BooleanField("Require Interpreter", default=False)
	password            = PasswordField("Password", [validators.Length(min=6, max=25)])
	roles               = SelectField("Your Roles", choices=list_roles)

@profile.route("/profile/<int:user_id>")
def show_profile(user_id: int):
	user = User.query.get_or_404(user_id)
	return render_template("profile/profile.html")

@profile.route("/profile/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
def edit_profile(user_id: int):
	if user_id != current_user.id:
		abort(403)

	form = EditProfileForm()

	if form.validate_on_submit():
		current_user.username = request.form.get("username")
		current_user.first_name = request.form.get("first_name")
		current_user.last_name = request.form.get("last_name")
		current_user.hearing_impaired = request.form.get("hearing_impaired")
		current_user.need_interpreter = request.form.get("require_interpreter")
		current_user.password = generate_password_hash(request.form.get("password")).encode()
		current_user.roles = Role.query.where(Role.role_name.in_(request.form.get("roles"))).all()

		save_db()

		return render_template("profile/edit.html", form=form)

	form.username.default = current_user.username
	form.first_name.default = current_user.first_name
	form.last_name.default = current_user.last_name
	form.hearing_impaired.default = current_user.hearing_impaired
	form.require_interpreter.default = current_user.need_interpreter
	form.roles.default = [(r.role_name, r.role_description) for r in current_user.roles]

	return render_template("profile/edit.html", form=form)
