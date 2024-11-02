import datetime
from typing import Optional

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
	roles: Mapped[list["Role"]] = relationship()


class Ideas(db.Model):
	owner: Mapped["User"] = relationship()
	description: Mapped[str]
	hearing_impaired_only: Mapped[bool]
	asl_fluent_only: Mapped[bool]
	desired_roles: Mapped[list["Role"]] = relationship()
	started: Mapped[bool]
	searching_for_contributors: Mapped[bool]
	finished: Mapped[bool]
	contributors: Mapped["User"] = relationship()


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
	return User