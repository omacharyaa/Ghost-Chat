import os
from datetime import timedelta


class Config:
	SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24))
	SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///ghost_chat.db")
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# SocketIO message queue (optional; can use Redis in production)
	SOCKETIO_MESSAGE_QUEUE = os.getenv("SOCKETIO_MESSAGE_QUEUE")

	# Session
	REMEMBER_COOKIE_DURATION = timedelta(days=7)

	# Email (optional for password reset)
	MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
	MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
	MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
	MAIL_USERNAME = os.getenv("MAIL_USERNAME")
	MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
	MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", os.getenv("MAIL_USERNAME"))

	# Geolocation API
	IPINFO_TOKEN = os.getenv("IPINFO_TOKEN")

	# Cleanup
	MESSAGE_TTL_HOURS = int(os.getenv("MESSAGE_TTL_HOURS", "24"))


class DevelopmentConfig(Config):
	DEBUG = True


class ProductionConfig(Config):
	DEBUG = False


config_by_name = {
	"development": DevelopmentConfig,
	"production": ProductionConfig,
}


def get_config() -> type[Config]:
	env = os.getenv("FLASK_ENV", "development").lower()
	return config_by_name.get(env, DevelopmentConfig)
