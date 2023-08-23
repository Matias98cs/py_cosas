import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_restful import Resource, reqparse, Api
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash,generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange

# Definir el formulario de contacto
class ContactForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    email = StringField('Correo Electrónico', validators=[DataRequired()])
    message = StringField('Mensaje', validators=[DataRequired()])
    submit = SubmitField('Enviar')

app = Flask(__name__)
app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

users = [
    {"username": "user1", "password": generate_password_hash("pass1")},
    {"username": "user2", "password": generate_password_hash("pass2")}
]

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = next((u for u in users if u['username'] == username), None)
        if user and check_password_hash(user['password'], password):
            user_obj = User()
            user_obj.id = username
            login_user(user_obj)
            return redirect(url_for('index'))
        else:
            flash("Credenciales no válidas. Intente nuevamente.", 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        # Aquí puedes manejar el envío del formulario, por ejemplo, enviar un correo electrónico
        # y luego redirigir a otra página o mostrar un mensaje de éxito.
        session['name'] = form.name.data
        flash('Formulario enviado con éxito', 'success')
        return redirect(url_for('index')) 

    return render_template('contact.html', form=form)

@app.route('/about')
@login_required
def about():
    return render_template('about.html')

@app.route('/calificaciones')
@login_required
def calificaciones():
    return render_template('calificaciones.html')

# Manejar rutas no válidas
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# APIS

calificaciones = [
    {"id": 1,"Nombre": 'Jose', "Clase": "Matemáticas", "Materia": "Álgebra", "Calificacion": 85},
    {"id": 2,"Nombre": 'Jose', "Clase": "Tecnología", "Materia": "Biología", "Calificacion": 92},
    {"id": 3,"Nombre": 'Jose', "Clase": "Historia", "Materia": "Geografía", "Calificacion": 78},
    {"id": 4,"Nombre": 'Jose', "Clase": "Arte", "Materia": "Pintura", "Calificacion": 95},
    {"id": 5,"Nombre": 'Jose', "Clase": "Música", "Materia": "Piano", "Calificacion": 88},
    {"id": 6,"Nombre": 'Jose', "Clase": "Deportes", "Materia": "Fútbol", "Calificacion": 70},
    {"id": 7,"Nombre": 'Jose', "Clase": "Idiomas", "Materia": "Inglés", "Calificacion": 90},
    {"id": 8,"Nombre": 'Jose', "Clase": "Ciencias", "Materia": "Física", "Calificacion": 82},
    {"id": 9,"Nombre": 'Pedro', "Clase": "Matemáticas", "Materia": "Álgebra", "Calificacion": 78},
    {"id": 10,"Nombre": 'Pedro', "Clase": "Tecnología", "Materia": "Biología", "Calificacion": 73},
    {"id": 11,"Nombre": 'Pedro', "Clase": "Historia", "Materia": "Geografía", "Calificacion": 68},
    {"id": 12,"Nombre": 'Pedro', "Clase": "Arte", "Materia": "Pintura", "Calificacion": 91},
    {"id": 13,"Nombre": 'Pedro', "Clase": "Música", "Materia": "Piano", "Calificacion": 73},
    {"id": 14,"Nombre": 'Pedro', "Clase": "Deportes", "Materia": "Fútbol", "Calificacion": 79},
    {"id": 15,"Nombre": 'Pedro', "Clase": "Idiomas", "Materia": "Inglés", "Calificacion": 91},
    {"id": 16,"Nombre": 'Pedro', "Clase": "Ciencias", "Materia": "Física", "Calificacion": 59}
]

# Definir el analizador de argumentos para las solicitudes POST
post_parser = reqparse.RequestParser()
post_parser.add_argument("Nombre", type=str, required=True, help="Nombre es requerido.")
post_parser.add_argument("Clase", type=str, required=True, help="Clase es requerida.")
post_parser.add_argument("Materia", type=str, required=True, help="Materia es requerida.")
post_parser.add_argument("Calificacion", type=int, required=True, help="Calificación es requerida.")

class CalificacionesResource(Resource):
    method_decorators= [login_required]
    
    def get(self):
        return calificaciones, 200

    def post(self):
        args = post_parser.parse_args()
        calificacion_id=0
        if calificaciones:
             calificacion_id=calificaciones[-1]['id'] + 1

        calificacion = {
                "id": calificacion_id,
                "Nombre": args['Nombre'],
                "Clase": args['Clase'],
                "Materia": args['Materia'],
                "Calificacion": args['Calificacion']
        }
        calificaciones.append(calificacion)
        return calificaciones, 201

    def delete(self, calificacion_id):
        global calificaciones

        calificacion = next((c for c in calificaciones if c['id'] == calificacion_id), None)
        if calificacion:
            calificaciones = [c for c in calificaciones if c['id'] != calificacion_id]
            return calificaciones, 201
        else:
            return calificaciones, 404
        
# Configurar la API
api = Api(app)
api.add_resource(CalificacionesResource, '/api/calificaciones', '/api/calificaciones/<int:calificacion_id>')

if __name__ == '__main__':
    app.run(debug=True)

