from __future__ import annotations

from flask import Flask
from .extensions import db, login_manager, migrate, socketio


def create_app() -> Flask:
	app = Flask(__name__, instance_relative_config=False)

	# Config
	from config import get_config
	app.config.from_object(get_config())

	# Extensions
	db.init_app(app)
	migrate.init_app(app, db)
	login_manager.init_app(app)
	socketio.init_app(
		app,
		message_queue=app.config.get("SOCKETIO_MESSAGE_QUEUE"),
		cors_allowed_origins="*",
	)

	# Ensure tables exist (first-run convenience)
	with app.app_context():
		# Import models so SQLAlchemy is aware of tables
		from . import models  # noqa: F401
		db.create_all()

		# Lightweight migration for SQLite: add missing profile columns if DB pre-existed
		try:
			from sqlalchemy import inspect, text
			engine = db.engine
			if engine.dialect.name == "sqlite":
				insp = inspect(engine)
				cols = {c["name"] for c in insp.get_columns("profiles")}
				if "name" not in cols:
					db.session.execute(text("ALTER TABLE profiles ADD COLUMN name VARCHAR(80)"))
				if "height_cm" not in cols:
					db.session.execute(text("ALTER TABLE profiles ADD COLUMN height_cm INTEGER"))
				db.session.commit()
		except Exception:
			# Best effort; ignore if table doesn't exist yet or other DBs
			pass

	# Login
	login_manager.login_view = "auth.login"

	# Blueprints and routes
	from .routes import register_blueprints
	register_blueprints(app)

	return app
