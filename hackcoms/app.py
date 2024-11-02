from flask import Flask
from db import db

def create_app() -> Flask:
	app = Flask(__name__)

	app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:pgpassword@0.0.0.0"

	db.init_app(app)

	return app

def setup_databases(app: Flask):
	with app.app_context():
	    db.create_all()

if __name__ == "__main__":
	setup_databases(create_app())