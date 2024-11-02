import datetime
from typing import Optional, Tuple

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash

class Base(DeclarativeBase):
	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

db = SQLAlchemy(model_class=Base)

class Role(db.Model):
	role_name: Mapped[str]
	role_description: Mapped[str]


class User(UserMixin, db.Model):
	__tablename__ = "user_account"

	username: Mapped[str] = mapped_column(unique=True)
	password: Mapped[bytes]
	first_name: Mapped[str]
	last_name: Mapped[str]
	hearing_impaired: Mapped[bool]
	need_interpreter: Mapped[bool]
	understand_asl: Mapped[bool]
	roles: Mapped[list["Role"]] = relationship()


class Ideas(db.Model):
	owner: Mapped["User"] = relationship()
	name: Mapped[str]
	description: Mapped[str]
	asl_fluent_only: Mapped[bool]
	desired_roles: Mapped[list["Role"]] = relationship()
	started: Mapped[bool]
	searching_for_contributors: Mapped[bool]
	finished: Mapped[bool]
	contributors: Mapped[list["User"]] = relationship()
	creation_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Message(db.Model):
	target_id: Mapped[int]
	room_type: Mapped[int]
	content: Mapped[str]
	invite: Mapped[Optional[int]]
	timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

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
		need_interpreter = need_interpreter
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
		desired_roles = Role.query.where(Role.role_name.in_([desired_roles])).all(),
		started = False,
		searching_for_contributors = True,
		finished = False,
		contributors = []
	)

	db.session.add(idea)
	db.session.commit()

	return idea

def list_roles() -> list[Tuple[str, str]]:
	return [(r.role_name, r.role_description) for r in Role.query.all()]