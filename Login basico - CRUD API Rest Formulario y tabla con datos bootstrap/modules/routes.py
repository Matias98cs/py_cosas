from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from modules.auth import login_required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange
import datetime

main_routes = Blueprint('main_routes', __name__)

# Definir el formulario de contacto
class ContactForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    email = StringField('Correo Electrónico', validators=[DataRequired()])
    message = StringField('Mensaje', validators=[DataRequired()])
    submit = SubmitField('Enviar')


@main_routes.route('/')
def index():
    return redirect(url_for('auth_routes.login'))

@main_routes.route('/dashboard', endpoint='dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main_routes.route('/about',endpoint='about')
@login_required
def about():
    return render_template('about.html')

@main_routes.route('/contact', methods=['GET', 'POST'],endpoint='contact')
@login_required
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        # Aquí puedes manejar el envío del formulario, por ejemplo, enviar un correo electrónico
        # y luego redirigir a otra página o mostrar un mensaje de éxito.
        session['name'] = form.name.data
        flash('Formulario enviado con éxito', 'success')
        return redirect(url_for('main_routes.dashboard'))

    return render_template('contact.html', form=form)

@main_routes.route('/calificaciones', endpoint='calificaciones')
@login_required
def calificaciones():
    return render_template('calificaciones.html')
