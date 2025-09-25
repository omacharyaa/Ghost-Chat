from __future__ import annotations

from datetime import datetime
from typing import Optional
import secrets
import string

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db, login_manager


class User(UserMixin, db.Model):
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255), unique=True, nullable=False, index=True)
	password_hash = db.Column(db.String(255), nullable=False)
	is_admin = db.Column(db.Boolean, default=False, nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

	messages = db.relationship("Message", backref="user", lazy=True)
	reports = db.relationship("Report", backref="reporter", lazy=True)
	profile = db.relationship("Profile", backref="user", uselist=False, cascade="all, delete-orphan")

	@property
	def password(self) -> str:  # type: ignore[override]
		raise AttributeError("Password is write-only")

	@password.setter
	def password(self, value: str) -> None:
		self.password_hash = generate_password_hash(value)

	def verify_password(self, password: str) -> bool:
		return check_password_hash(self.password_hash, password)


class Profile(db.Model):
	__tablename__ = "profiles"

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
	name = db.Column(db.String(80), nullable=True)
	gender = db.Column(db.String(20), nullable=True)
	age = db.Column(db.Integer, nullable=True)
	height_cm = db.Column(db.Integer, nullable=True)
	interests = db.Column(db.Text, nullable=True)
	updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
	return db.session.get(User, int(user_id))


def _generate_unique_code(length: int = 6) -> str:
	alphabet = string.ascii_uppercase + string.digits
	return "".join(secrets.choice(alphabet) for _ in range(length))


class Group(db.Model):
	__tablename__ = "groups"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	code = db.Column(db.String(12), unique=True, nullable=False, index=True)
	region = db.Column(db.String(64), nullable=True)
	created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

	@staticmethod
	def create_unique(name: str, region: Optional[str], created_by: Optional[int]) -> "Group":
		code = _generate_unique_code()
		while Group.query.filter_by(code=code).first() is not None:
			code = _generate_unique_code()
		g = Group(name=name, code=code, region=region, created_by=created_by)
		return g


class Message(db.Model):
	__tablename__ = "messages"

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
	room = db.Column(db.String(64), nullable=False, index=True)
	region = db.Column(db.String(64), nullable=False, index=True)
	nickname = db.Column(db.String(64), nullable=True)
	content = db.Column(db.Text, nullable=True)
	image_url = db.Column(db.String(512), nullable=True)
	created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True, nullable=False)

	reactions = db.relationship("Reaction", backref="message", cascade="all, delete-orphan")
	reports = db.relationship("Report", backref="message", cascade="all, delete-orphan")


class Reaction(db.Model):
	__tablename__ = "reactions"

	id = db.Column(db.Integer, primary_key=True)
	message_id = db.Column(db.Integer, db.ForeignKey("messages.id"), nullable=False, index=True)
	emoji = db.Column(db.String(16), nullable=False)
	count = db.Column(db.Integer, nullable=False, default=1)


class Report(db.Model):
	__tablename__ = "reports"

	id = db.Column(db.Integer, primary_key=True)
	message_id = db.Column(db.Integer, db.ForeignKey("messages.id"), nullable=False, index=True)
	reporter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
	reason = db.Column(db.String(255), nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
