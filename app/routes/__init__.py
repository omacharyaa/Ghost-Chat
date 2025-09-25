from __future__ import annotations

from flask import Flask

from .auth import auth_bp
from .main import main_bp
from .admin import admin_bp
from .groups import groups_bp
from .profile import profile_bp
from .. import sockets  # noqa: F401  (register socket events)


def register_blueprints(app: Flask) -> None:
	app.register_blueprint(auth_bp)
	app.register_blueprint(main_bp)
	app.register_blueprint(admin_bp)
	app.register_blueprint(groups_bp)
	app.register_blueprint(profile_bp)
