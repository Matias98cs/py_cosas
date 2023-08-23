from flask import redirect, url_for, request, flash, render_template, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from modules.models.entities import User
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    if "/api/" in request.path:
        return abort(401)
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('routes.index'))
        else:
            flash("Credenciales no válidas. Intente nuevamente.", 'danger')

    usuario=User(username="user3", password="pass3")
    usuario.guardar()
    #db.session.add(usuario)
    #db.session.commit()
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
