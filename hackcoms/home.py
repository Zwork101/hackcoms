from datetime import datetime

from hackcoms.db import Ideas

from flask import Blueprint, render_template
import pytz

home = Blueprint("home", __name__)

def idea_weight(idea: Ideas):
	value = 10 + (10 * len(idea.contributors))
	current_time = datetime.now()
	time_diff = datetime.now(pytz.utc) - idea.creation_date
	value += 5 * min(0, 14 - time_diff.days)
	return value

@home.route("/")
def index():
	wip_ideas = Ideas.query.where(Ideas.searching_for_contributors.is_(True)).all()
	wip_ideas.sort(key=idea_weight, reverse=True)

	finished_ideas = Ideas.query.where(Ideas.finished.is_(True)).all()

	return render_template("index.html", projects=wip_ideas[:10], finished=finished_ideas[:10])