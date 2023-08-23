from flask import Blueprint, render_template, redirect, url_for, request, session, flash, g
from flask_restful import Resource
import datetime

auth_routes = Blueprint('auth_routes', __name__)

users = [
    {"username": "user1", "password": "pass1"},
    {"username": "user2", "password": "pass2"}
]

# Función para comprobar si el usuario ha iniciado sesión
def find_user_by_username(users_list, username_to_find, password):
    return next((user for user in users_list if user["username"] == username_to_find and user["password"] == password), None)

# Función para validar las credenciales y devolver los datos del usuario si son válidos
def is_logged_in():
    if 'username' in session:
        session.permanent = True
        g.user = True
        return True
    g.user = False
    return False

# Decorador personalizado para hacer cumplir el requisito de inicio de sesión para ciertas rutas
def login_required(f):
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('auth_routes.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Decorador personalizado para hacer cumplir el requisito de inicio de sesión para los endpoints de la API
def api_login_required(f):
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return {'message': 'Unauthorized'}, 401
        return f(*args, **kwargs)
    return decorated_function

# Login route
@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if find_user_by_username(users, username, password):
            session['username'] = username
            return redirect(url_for('main_routes.dashboard'))
        flash("Credenciales no válidas. Intente nuevamente.", 'danger')

    if is_logged_in():
        return redirect(url_for('main_routes.dashboard'))

    return render_template('login.html')

# Logout route
@auth_routes.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('auth_routes.login'))
