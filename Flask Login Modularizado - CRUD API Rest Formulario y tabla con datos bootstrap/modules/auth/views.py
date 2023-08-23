from . import auth_bp
from flask import redirect, url_for, request, flash, render_template
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from modules.models import User

users = [
    {"username": "user1", "password": generate_password_hash("pass1")},
    {"username": "user2", "password": generate_password_hash("pass2")}
]

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((u for u in users if u['username'] == username and check_password_hash(u['password'], password)), None)
        if user:
            user_obj = User()
            user_obj.id = username
            login_user(user_obj)
            return redirect(url_for('routes.index'))
        else:
            flash("Credenciales no válidas. Intente nuevamente.", 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
