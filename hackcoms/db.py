import datetime
from typing import Optional, Tuple

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)

db = SQLAlchemy(model_class=Base)

class Role(db.Model):
    role_name: Mapped[str]
    role_description: Mapped[str]
    users: Mapped[list["User"]] = relationship(
        secondary="user_roles", backref="roles", viewonly=True
    )
    ideas: Mapped[list["Ideas"]] = relationship("Ideas",
        secondary="idea_roles", backref="Role", viewonly=True
    )

class User(UserMixin, db.Model):
    __tablename__ = "user_account"

    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]
    first_name: Mapped[str]
    last_name: Mapped[str]
    hearing_impaired: Mapped[bool]
    need_interpreter: Mapped[bool]
    understand_asl: Mapped[bool]

class UserRole(db.Model):
    __tablename__ = "user_roles"

    user_id = Column(Integer, ForeignKey("user_account.id"))
    role_id = Column(Integer, ForeignKey("role.id"))

class IdeaRole(db.Model):
    __tablename__ = "idea_roles"

    idea_id = Column(Integer, ForeignKey("ideas.id"))
    role_id = Column(Integer, ForeignKey("role.id"))

class IdeaContributor(db.Model):
    __tablename__ = "idea_contributor"

    idea_id = Column(Integer, ForeignKey("ideas.id"))
    user_id = Column(Integer, ForeignKey("user_account.id"))    

class Ideas(db.Model):
    __tablename__ = "ideas"

    owner_id = Column(Integer, ForeignKey("user_account.id"))
    owner: Mapped['User'] = relationship('User', foreign_keys='Ideas.owner_id')
    name: Mapped[str]
    description: Mapped[str]
    asl_fluent_only: Mapped[bool]
    started: Mapped[bool]
    searching_for_contributors: Mapped[bool]
    finished: Mapped[bool]
    contributors: Mapped[list["User"]] = relationship(
        secondary="idea_contributor", backref="contribs", viewonly=True
    )
    needed_roles: Mapped[list["Role"]] = relationship("Role",
        secondary="idea_roles", backref="Ideas", viewonly=True
    )
    creation_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Message(db.Model):
    room_id = Column(Integer, ForeignKey("room.id"))
    sender_id = Column(Integer, ForeignKey("user_account.id"))
    room: Mapped["Room"] = relationship('Room', foreign_keys='Message.room_id')
    sender: Mapped["User"] = relationship('User', foreign_keys='Message.sender_id')
    content: Mapped[str]
    invite_id = Column(Integer, ForeignKey("invite.id"), nullable=True)
    invite: Mapped["Invite"] = relationship('Invite', foreign_keys='Message.invite_id')
    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

class UserRoom(db.Model):
    __tablename__ = "user_room"

    user_id = Column(Integer, ForeignKey("user_account.id"))
    room_id = Column(Integer, ForeignKey("room.id"))

class Room(db.Model):
    __tablename__ = "room"

    participants: Mapped[list["User"]] = relationship(
        secondary="user_room", backref="rooms"
    )

class Invite(db.Model):
    __tablename__ = "invite"

    idea_id = Column(Integer, ForeignKey("ideas.id"))
    idea: Mapped["Ideas"] = relationship('Ideas', foreign_keys='Invite.idea_id')
    target_id = Column(Integer, ForeignKey("user_account.id"))
    target: Mapped["User"] = relationship('User', foreign_keys='Invite.target_id')

def add_contributor(
    idea: Ideas,
    user: User
    ):
    
    ic = IdeaContributor(
        idea_id = idea.id,
        user_id = user.id
    )
    db.session.add(ic)
    db.session.commit()

def create_invite(
    idea_id: int,
    target: User
    ) -> Invite:
    invite = Invite(
        idea_id = int(idea_id),
        target_id = int(target)
    )
    db.session.add(invite)
    db.session.commit()
    return invite

def create_room(
    *participants: User
    ) -> Room:
    room = Room()
    db.session.add(room)
    db.session.commit()

    db.session.bulk_save_objects([
        UserRoom(
            user_id=p.id, room_id=room.id
        ) for p in participants
    ])
    db.session.commit()
    return room

def create_user(
    username: str, 
    password: str, 
    first_name: str,
    last_name: str,
    hearing_impaired: bool,
    need_interpreter: bool,
    ) -> User:
    user = User(
        username = username,
        password = generate_password_hash(password).encode(),
        first_name = first_name,
        last_name = last_name,
        hearing_impaired = hearing_impaired,
        need_interpreter = need_interpreter,
        understand_asl = False  #  TODO: Get this value
    )

    db.session.add(user)
    db.session.commit()

    return user

def create_idea(
    owner: User,
    description: str,
    name: str,
    asl_only: bool,
    desired_roles: list[str]
    ) -> Ideas:

    idea = Ideas(
        owner = owner,
        name = name,
        description = description,
        asl_fluent_only = asl_only,
        started = False,
        searching_for_contributors = True,
        finished = False,
    )

    db.session.add(idea)
    db.session.commit()

    role_ids = [int(role_id) for role_id in desired_roles]
    roles = [
        IdeaRole(
            idea_id = idea.id,
            role_id = rid
        ) for rid in role_ids
    ]
    db.session.bulk_save_objects(roles)
    db.session.commit()

    return idea

def list_roles() -> list[Tuple[str, str]]:
    return [(r.id, r.role_name) for r in Role.query.all()]

def save_db():
    db.session.commit()

def create_message(
    room: Room,
    sender: User,
    content: str,
    invite: int | None = None
    ) -> Message:

    if invite is not None:
        msg = Message(
            room = room,
            sender = sender,
            content = content,
            invite_id = invite
        )
    else:
        msg = Message(
            room = room,
            sender = sender,
            content = content,
        )

    db.session.add(msg)
    db.session.commit()

    return msg
