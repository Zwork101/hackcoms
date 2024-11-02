from db import db
from auth import login_manager
from messages import msgio

from flask import Flask

def create_app() -> Flask:
	app = Flask(__name__)

	app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:pgpassword@0.0.0.0"
	login_manager.login_view = 'auth.login'

	login_manager.init_app(app)
	db.init_app(app)
	msgio.init_app(app)

	return app

def setup_databases(app: Flask):
	with app.app_context():
	    db.create_all()

if __name__ == "__main__":
	setup_databases(create_app())