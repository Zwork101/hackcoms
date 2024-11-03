import functools

from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField

from db import Ideas, Invite, Message, Room, User, add_contributor, create_invite, create_message, create_room

from bleach import clean
from flask import abort, Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from flask_socketio import SocketIO, disconnect, emit, join_room

messages = Blueprint("messages", __name__)
msgio = SocketIO()

# TODO: Add XSS protection to username

class RoomForm(FlaskForm):
	target_user = HiddenField()

class InviteForm(FlaskForm):
	idea = SelectField("Idea", choices=[])
	target = HiddenField()
	room = HiddenField()

@messages.route("/invite/accept/<int:invite_id>")
@login_required
def accept_invite(invite_id: int):
	invite = Invite.query.get_or_404(invite_id)
	print(invite.target.id, current_user.id)
	if invite.target != current_user:
		abort(403)
	add_contributor(invite.idea, current_user)

	return redirect(url_for("ideas.idea_page", idea_id=invite.idea.id))

@messages.route("/invite", methods=["POST"])
@login_required
def make_invite():
	form = InviteForm()
	form.idea.choices = [
		(i.id, i.name) for i in Ideas.query.where(Ideas.owner_id == current_user.id).all()
	]

	if form.validate_on_submit():
		idea = Ideas.query.get_or_404(request.form.get("idea"))
		room = Room.query.get_or_404(request.form.get("room"))
		invite = create_invite(request.form.get("idea"), request.form.get("target"))
		_ = create_message(room, current_user, f"Project Invite for {idea.name} 👍", invite=invite.id)

		return redirect(url_for("messages.message_room", room_id = request.form.get("room")))

	abort(400)

@messages.route("/messages")
@login_required
def list_messages():
	user_rooms = Room.query.where(Room.participants.contains(current_user)).all()

	rendered_rooms = [
	(", ".join(p.username for p in room.participants if p.id != current_user.id), room.id) 
		for room in user_rooms
	]

	return render_template("messages/list.html", rooms=rendered_rooms)

@messages.route("/messages/new", methods=["POST"])
@login_required
def new_room():
	form = RoomForm()

	if form.validate_on_submit():
		target_user = User.query.get_or_404(request.form.get("target_user"))
		room = create_room(target_user, current_user)

		return redirect(url_for("messages.message_room", room_id=room.id))

	abort(400, "Unable to validate data")

@messages.route("/messages/<int:room_id>", methods=["GET"])
@login_required
def message_room(room_id: int):

	user_room = Room.query.get(room_id)

	if current_user not in user_room.participants:
		abort(401)

	form = InviteForm(
		target=next(p.id for p in user_room.participants if p != current_user),
		room=room_id
	)

	form.idea.choices = [
		(i.id, i.name) for i in Ideas.query.where(Ideas.owner_id == current_user.id).all()
	]

	messages = Message.query.where(Message.room_id == user_room.id)

	return render_template("messages/chat.html", messages=messages, room=user_room, form=form)


# Credit SocketIO Flask docs
def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped

@msgio.on('connect')
@authenticated_only
def welcome_client(auth):
	room_id = int(request.headers['Referer'].split("/")[-1])
	room = Room.query.get_or_404(room_id)

	if current_user not in room.participants:
		abort(401)

	join_room(room.id)

@msgio.on('message')
@authenticated_only
def ws_msg(data):
	print("Message Data:", data, type(data))
	room = Room.query.get_or_404(data['room'])

	if current_user not in room.participants:
		abort(401)

	create_message(room, current_user, data['message'])
	emit("message", {
		"message": clean(data['message']),
		"author": current_user.username
		}, to=room.id)