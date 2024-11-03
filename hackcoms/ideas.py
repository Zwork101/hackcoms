from datetime import datetime

from db import Ideas, list_roles, create_idea
from messages import RoomForm

from flask import abort, Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
import pytz
from wtforms import BooleanField, SelectMultipleField, SelectMultipleField, StringField
from wtforms.validators import Length

ideas = Blueprint("ideas", __name__)

def idea_weight(idea: Ideas):
	value = 10 + (10 * len(idea.contributors))
	current_time = datetime.now()
	time_diff = datetime.now(pytz.utc) - idea.creation_date
	value += 5 * min(0, 14 - time_diff.days)
	return value


class IdeaForm(FlaskForm):
	name                  = StringField("Idea Name", [Length(min=6, max=28)])
	description           = StringField("Idea Description", [Length(min=10, max=2000)])
	asl_only              = BooleanField("ASL Fluency Required")
	roles_needed          = SelectMultipleField("Required Roles", choices=list_roles)

@ideas.route("/idea/<int:idea_id>")
def idea_page(idea_id: int):
	idea = Ideas.query.get(idea_id)
	form = RoomForm(target_user=idea.owner.id)
	# form.target_user.default = 
	# import pdb; pdb.set_trace()

	if not idea:
		abort(404, "Unable to find Idea")

	return render_template("ideas/idea.html", idea=idea, form=form)

@ideas.route("/idea", methods=["GET", "POST"])
@login_required
def idea_creation():
	form = IdeaForm()

	if form.validate_on_submit():

		idea = create_idea(
			current_user,
			request.form.get("description"),
			request.form.get("name"),
			bool(request.form.get("asl_only")),
			request.form.getlist("roles_needed")
		)

		return redirect(url_for("ideas.idea_page", idea_id=idea.id))

	return render_template("ideas/make.html", form=form)

@ideas.route("/idea-list")
@ideas.route("/idea-list/<int:pagination>")
def list_ideas(pagination: int | None = None):
	# This stuff should get cached
	all_ideas = Ideas.query.where(Ideas.searching_for_contributors.is_(True)).all()
	all_ideas.sort(key=idea_weight, reverse=True)

	if pagination is None:
		pagination = 0

	idea_selection = all_ideas[(pagination * 20):(pagination * 20 + 20)]

	return render_template("ideas/list.html", ideas=idea_selection)