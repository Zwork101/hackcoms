import functools

from flask_wtf import FlaskForm
from wtforms import HiddenField

from db import Message, Room, User, create_message, create_room

from flask import abort, Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from flask_socketio import SocketIO, disconnect, join_room, send

messages = Blueprint("messages", __name__)
msgio = SocketIO()

class RoomForm(FlaskForm):
	target_user = HiddenField()

@messages.route("/messages")
@login_required
def list_messages():
	user_rooms = Room.query.where(Room.participants.contains(current_user)).all()

	rendered_rooms = [
	(", ".join(p for p in room.participants if p.id != current_user.id), room.id) 
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

	messages = Message.query.where(Message.room_id == user_room.id)

	return render_template("messages/chat.html", messages=messages, room=user_room)


# Credit SocketIO Flask docs
def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped

@msgio.on('join')
@authenticated_only
def ws_join(data):
	room = Room.query.get_or_404(data['room'])

	if current_user not in room.participants:
		abort(401)

	join_room(room.id)

@msgio.on('message')
@authenticated_only
def ws_msg(data):
	room = Room.query.get_or_404(data['room'])

	if current_user not in room.participants:
		abort(401)

	create_message(room, current_user, data['message'], data.get('invite', False))
	send(data['message'], to=room.id)