from flask import redirect, url_for
from flask_login import LoginManager
from modules.models import User

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))
