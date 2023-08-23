import os
from flask import Flask
from flask_restful import Api
from modules.auth.views import auth_bp
from modules.routes.views import routes_bp, page_not_found
from modules.api.calificaciones import CalificacionesResource
from auth_manager import login_manager

app = Flask(__name__)
app.secret_key = os.urandom(24)

login_manager.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(routes_bp)
app.register_error_handler(404, page_not_found)

api = Api(app)
api.add_resource(CalificacionesResource, '/api/calificaciones', '/api/calificaciones/<int:calificacion_id>')

if __name__ == '__main__':
    app.run(debug=True)

