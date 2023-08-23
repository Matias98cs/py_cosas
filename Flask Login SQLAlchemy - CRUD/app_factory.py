import os
from flask import Flask
from flask_restful import Api
from modules.auth import auth_bp, login_manager
from modules.routes import routes_bp, page_not_found
from modules.apis.calificaciones import CalificacionesResource
from modules.apis.personas import PersonasResource
from modules.models.base import db 
from config import db_connector, db_user, db_password, db_ip_address, db_name

def create_app():
	app = Flask(__name__)
	app.secret_key = os.urandom(24)
	app.config['SQLALCHEMY_DATABASE_URI'] = f"{db_connector}://{db_user}:{db_password}@{db_ip_address}/{db_name}"

	db.init_app(app)
	api=Api(app)
	login_manager.init_app(app)
	
	with app.app_context():
		db.create_all()

	app.register_blueprint(auth_bp)
	app.register_blueprint(routes_bp)
	app.register_error_handler(404, page_not_found)
	api.add_resource(CalificacionesResource, '/api/calificaciones', '/api/calificaciones/<int:calificacion_id>')
	api.add_resource(PersonasResource, '/api/personas', '/api/personas/<int:persona_id>')

	return app
