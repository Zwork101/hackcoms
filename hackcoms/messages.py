import functools

from db import Message, Room, create_message

from flask import abort, Blueprint, render_template
from flask_login import login_required, current_user
from flask_socketio import SocketIO, disconnect, join_room, send

messages = Blueprint("messages", __name__)
msgio = SocketIO()

@messages.route("/messages")
@login_required
def list_messages():
	user_rooms = Room.query.where(Room.participants.contains(current_user)).order_by(Room.latest_message.desc()).all()

	rendered_rooms = [
	(", ".join(p for p in room.participants if p.id != current_user.id), room.latest_message.content[:200], room.id) 
		for room in user_rooms
	]

	return render_template("messages/list.html", rooms=rendered_rooms)

@messages.route("/messages/<room_id:int>")
@login_required
def message_room(room_id: int):
	user_room = Room.query.get_or_404(room_id)

	if current_user not in user_room.participants:
		abort(401)

	messages = Message.query.where(Message.room.is_(user_room))

	return render_template("messages/chat.html", messages=messages)


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
def ws_join(data):
	room = Room.query.get_or_404(data['room'])

	if current_user not in room.participants:
		abort(401)

	create_message(room, current_user, data['message'], data.get('invite', False))
	send(data['message'], to=room.id)