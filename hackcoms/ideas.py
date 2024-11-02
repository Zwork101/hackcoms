from datetime import datetime

from db import Ideas, list_roles, create_idea

from flask import abort, Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, StringField
from wtforms.validators import Length

ideas = Blueprint("ideas", __name__)

def idea_weight(idea: Ideas):
	value = 10 + (10 * len(idea.contributors))
	current_time = datetime.now()
	time_diff = datetime.now() - idea.creation_date
	value += 5 * min(0, 14 - time_diff.days)
	return value


class IdeaForm(FlaskForm):
	name                  = StringField("Idea Name", [Length(min=6, max=28)])
	description           = StringField("Idea Description", [Length(min=10, max=2000)])
	asl_only              = BooleanField("ASL Fluency Required")
	roles_needed          = SelectField("Required Roles", choices=list_roles)

@ideas.route("/idea/<idea_id:int>")
def idea_page(idea_id: int):
	idea = Ideas.query.get(idea_id)

	if not idea:
		abort(404, error_msg="Unable to find Idea")

	return render_template("ideas/idea.html", idea=idea)

@ideas.route("/idea/new", methods=["POST"])
@login_required
def idea_creation():
	form = IdeaForm()

	if form.validate_on_submit():

		idea = create_idea(
			current_user,
			request.form.get("description"),
			request.form.get("name"),
			request.form.get("asl_only"),
			request.form.get("roles_needed")
		)

		return redirect(url_for("idea_page", idea_id=idea.id))

@ideas.route("/idea-list")
@ideas.route("/idea-list/<pagination:int>")
def list_ideas(pagination: int | None = None):
	# This stuff should get cached
	all_ideas = Ideas.query.where(Ideas.searching_for_contributors.is_(True)).all()
	all_ideas.sort(key=idea_weight, reverse=True)

	if pagination is None:
		pagination = 0

	idea_selection = all_ideas[(pagination * 20):(pagination * 20 + 20)]

	return render_template("ideas/list.html", ideas=idea_selection)