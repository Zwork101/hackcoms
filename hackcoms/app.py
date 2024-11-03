from os import environ

from db import User, create_user, db
from auth import login_manager, auth
from ideas import ideas
from messages import msgio, messages
from profile import profile
from home import home

from flask import Flask

def create_app() -> Flask:
	app = Flask(__name__, template_folder="../templates", static_folder="../static")

	app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:pgpassword@129.21.103.183"
	login_manager.login_view = 'auth.login'
	app.config['SECRET_KEY'] = "uhnfoquih4nfvq7hn :hq3v87qpv9893vh8 49q8u4vnp4q8q4098 h[qtv]"

	login_manager.init_app(app)
	db.init_app(app)
	msgio.init_app(app)

	app.register_blueprint(auth)
	app.register_blueprint(ideas)
	app.register_blueprint(messages)
	app.register_blueprint(profile)
	app.register_blueprint(home)

	return app

def setup_databases(app: Flask):
	with app.app_context():
	    db.create_all()

	    if User.query.get(1) is None:
	    	create_user("evan", "password", "Evan", "Mathewson", False, False)
	    	create_user("nathan", "password", "Nathan", "Zilora", False, False)
	    	create_user("bob", "password", "Bob", "Smith", True, False)
	    	create_user("alice", "password", "Alice", "Smith", False, False)
	    	create_user("hero", "password", "zwack", "zwack", True, True)
	    	create_user("villan", "password", "zwack", "zwack", True, False)
	    	create_user("coms", "password", "COMS", "@ RIT", True, True)

if __name__ == "__main__":
	app = create_app()
	setup_databases(app)
	app.run("0.0.0.0", port=8080, load_dotenv=True)