from flask import Blueprint, render_template,flash, request, jsonify, redirect, url_for
from flask_login import login_required
from modules.models.entities import Persona, Genero, Pais, Provincia, Ciudad, Barrio, Lugar
from flask import Blueprint
from math import ceil
from sqlalchemy import func
from config import registros_por_pagina
from datetime import datetime

personas_bp = Blueprint('routes_personas', __name__)

@personas_bp.route('/personas', methods=['GET'])
@login_required
def obtener_personas_paginadas():
    page = request.args.get('page', default=1, type=int)
    total_personas = Persona.query.count()
    total_paginas = ceil(total_personas / registros_por_pagina)
    personas = Persona.query.paginate(page=page, per_page=registros_por_pagina)
    return render_template('personas/personas.html', personas=personas, total_paginas=total_paginas)

@personas_bp.route('/personas/<int:persona_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_persona(persona_id):
    persona = Persona.query.get_or_404(persona_id)

    if request.method == 'POST':
        genero=Genero.crear_y_obtener(nombre=request.form['genero'])

        pais=Pais.crear_y_obtener(nombre=request.form['pais'])
        provincia=Provincia.crear_y_obtener(nombre=request.form['provincia'])
        ciudad=Ciudad.crear_y_obtener(nombre=request.form['ciudad'])
        barrio=Barrio.crear_y_obtener(nombre=request.form['barrio'])
        lugar=Lugar.crear_y_obtener(pais=pais,provincia=provincia,ciudad=ciudad, barrio=barrio)

        persona.nombre = request.form['nombre']
        persona.apellido = request.form['apellido']
        persona.email = request.form['email']
        persona.personal_id = request.form['personal_id']

        birthdate_str = request.form['birthdate']
        persona.birthdate = datetime.strptime(birthdate_str, '%d-%m-%Y').isoformat()
        persona.genero = genero
        persona.lugar = lugar

        resultado=persona.guardar()
        if resultado["Exito"]:
            flash('Persona actualizada correctamente', 'success')
        else:
            flash('Error al actualziar persona', 'warning')
        return redirect(url_for('routes_personas.obtener_personas_paginadas'))

    return render_template('personas/editar_persona.html', persona=persona)

@personas_bp.route('/personas/<int:persona_id>', methods=['POST'])
@login_required
def eliminar_persona(persona_id):
    persona = Persona.query.get_or_404(persona_id)
    resultado=persona.borrar()
    if resultado["Exito"]:
        flash('Persona eliminada correctamente', 'success')
    else:
        flash('Error al eliminar persona', 'success')
    return redirect(url_for('routes_personas.obtener_personas_paginadas'))

@personas_bp.route('/personas/crear', methods=['GET', 'POST'])
@login_required
def crear_persona():
    if request.method == 'POST':
        genero=Genero.crear_y_obtener(nombre=request.form['genero'])
        pais=Pais.crear_y_obtener(nombre=request.form['pais'])
        provincia=Provincia.crear_y_obtener(nombre=request.form['provincia'])
        ciudad=Ciudad.crear_y_obtener(nombre=request.form['ciudad'])
        barrio=Barrio.crear_y_obtener(nombre=request.form['barrio'])
        lugar=Lugar.crear_y_obtener(pais=pais,provincia=provincia,ciudad=ciudad, barrio=barrio)

        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        birthdate_str = request.form['birthdate']
        birthdate = datetime.strptime(birthdate_str, '%d-%m-%Y').isoformat()
        personal_id = request.form['personal_id']
        genero = genero
        lugar = lugar

        nueva_persona = Persona(nombre=nombre, apellido=apellido, email=email, birthdate=birthdate, personal_id=personal_id, genero=genero, lugar=lugar)

        resultado=nueva_persona.guardar()
        if resultado["Exito"]:
            flash('Persona creada correctamente', 'success')
        else:
            flash('Error al crear persona', 'warning')
        return redirect(url_for('routes_personas.obtener_personas_paginadas'))

    return render_template('personas/crear_persona.html')

