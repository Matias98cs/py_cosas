from helpers.database import obtener_session
from helpers.models import Persona, Genero, TipoPersona, Pais, Ciudad, Barrio, Provincia, Lugar, Programa, Facultad, Universidad, Campus, Carrera, personasCarreras
import pandas as pd

session_db = obtener_session()

profesoresDF = pd.read_csv("Profesores.csv")
alumnosDF = pd.read_csv("Alumnos.csv")
personasDF = pd.concat([profesoresDF, alumnosDF])

cursos_profesoresDF = pd.read_csv("cursos_profesores.csv")

lista_errores_personas = []
for _, datos in personasDF.iterrows():
    fila = {**datos}
    session_db.begin()
    try:
        # Se procesa la dirección de la persona, insertando si corresponde los items faltantes
        pais = Pais.crear_y_obtener(session_db, nombre=fila['country'])
        ciudad = Ciudad.crear_y_obtener(session_db, nombre=fila['city'])
        barrio = Barrio.crear_y_obtener(session_db, nombre=fila['town'])
        provincia = Provincia.crear_y_obtener(session_db, nombre=fila['state'])
        lugar = Lugar.crear_y_obtener(
            session_db, pais=pais, barrio=barrio, provincia=provincia, ciudad=ciudad)
        genero = Genero.crear_y_obtener(session_db, nombre=fila['gender'])

        # La persona se inserta al final porque se necesitan las entidades de genero y lugar ya cargadas
        persona = Persona.crear_y_obtener(session_db, nombre=fila['first_name'], apellido=fila['last_name'],
                                          email=fila['email'], birthdate=fila['birthdate'], personal_id=fila['personal_id'], lugar=lugar, genero=genero)
        session_db.commit()
    except:
        session_db.rollback()
        lista_errores_personas.append(fila)

lista_errores_cursos_profesores = []
for _, datos in cursos_profesoresDF.iterrows():
    fila = {**datos}
    session_db.begin()
    try:
        programa = Programa.crear_y_obtener(session_db, nombre=fila['program'])
        facultad = Facultad.crear_y_obtener(session_db, nombre=fila['branch'])
        universidad = Universidad.crear_y_obtener(
            session_db, nombre=fila['institute'])
        campus = Campus.crear_y_obtener(session_db, nombre=fila['campus'])
        carrera = Carrera.crear_y_obtener(
            session_db, programa=programa, facultad=facultad, universidad=universidad, campus=campus)
        rol = TipoPersona.crear_y_obtener(session_db, nombre='Profesor')
        persona = Persona.crear_y_obtener(
            session_db, personal_id=fila['instructor'])
        persona_carrera = personasCarreras.crear_y_obtener(
            session_db, persona=persona, carrera=carrera, tipopersona=rol)
        session_db.commit()
    except:
        session_db.rollback()
        lista_errores_cursos_profesores.append(fila)

lista_errores_cursos_alumnos = []
for _, datos in alumnosDF.iterrows():
    fila = {**datos}
    session_db.begin()
    try:
        persona = Persona.crear_y_obtener(
            session_db, personal_id=fila['personal_id'])
        programa = Programa.crear_y_obtener(session_db, nombre=fila['program'])
        carrera = Carrera.crear_y_obtener(session_db, programa=programa)
        rol = TipoPersona.crear_y_obtener(session_db, nombre='Alumno')
        persona_carrera = personasCarreras.crear_y_obtener(
            session_db, persona=persona, carrera=carrera, tipopersona=rol)
        session_db.commit()
    except:
        session_db.rollback()
        lista_errores_cursos_alumnos.append(fila)

print(lista_errores_personas)
print(lista_errores_cursos_profesores)
print(lista_errores_cursos_alumnos)
session_db.close()
