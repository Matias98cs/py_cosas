# pip install flask-restful
# pip install flask-session

import os
import datetime 
from flask import Flask
from flask_session import Session
from flask_restful import Api
from modules.routes import main_routes
from modules.auth import auth_routes

from modules.api import CalificacionesResource

app = Flask(__name__)

# Configuraciones
app.config['FLASH_MESSAGES'] = True
app.config['FLASH_MESSAGES_CATEGORY'] = 'message'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=15)
Session(app)

# Registrar rutas de autenticación desde auth_routes
app.register_blueprint(auth_routes)
# Registrar rutas principales desde main_routes
app.register_blueprint(main_routes)

# Configurar la API
api = Api(app)
api.add_resource(CalificacionesResource, '/api/calificaciones', '/api/calificaciones/<int:calificacion_id>')


if __name__ == '__main__':
    app.run(debug=True)