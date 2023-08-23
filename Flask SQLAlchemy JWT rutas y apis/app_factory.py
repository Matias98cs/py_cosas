import os
from flask import Flask
from flask_restful import Api
from modules.auth import auth_bp, login_manager
from modules.routes import routes_bp, page_not_found
from modules.routes_personas import personas_bp
from modules.apis.personas import PersonasResource
from modules.apis.lugares import LugaresResource
from modules.models.base import db 
from config import db_connector, db_user, db_password, db_ip_address, db_name
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import JWTManager
from modules.auth import csrf

def create_app():
	app = Flask(__name__)
	app.secret_key = os.urandom(24)
	app.config['SQLALCHEMY_DATABASE_URI'] = f"{db_connector}://{db_user}:{db_password}@{db_ip_address}/{db_name}"

	db.init_app(app)
	api=Api(app)
	csrf.init_app(app)
	jwt = JWTManager(app)
	login_manager.init_app(app)
	
	#with app.app_context():
	#	db.create_all()

	app.register_blueprint(auth_bp)
	app.register_blueprint(routes_bp)
	app.register_blueprint(personas_bp)
	app.register_error_handler(404, page_not_found)
	api.add_resource(PersonasResource, '/api/personas', '/api/personas/<int:persona_id>')
	api.add_resource(LugaresResource, '/api/lugares')

	return app
