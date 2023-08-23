from database import crear_conexion, obtener_session
from models import Base, Persona, Genero, TipoPersona, Barrio, Pais, Provincia, Ciudad, Lugar, Programa, Facultad, Universidad, Campus, Carrera, PersonasCarreras
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Date, ForeignKey, case, and_, or_, extract, UniqueConstraint, func


base_general = "PruebaTrabajo"
engine_mysql = crear_conexion(
    "mysql", "root", "Matias45566", "localhost", base_general)

Base.metadata.create_all(engine_mysql)
session_mysql = obtener_session(engine_mysql)


profesoresDF = pd.read_csv("Profesores.csv")
# Agregamos esta nueva columna con la constante profesor en el tipo de persona para este DF
profesoresDF["tipopersona"] = "profesor"

alumnosDF = pd.read_csv("Alumnos.csv")
# Agregamos esta nueva columna con la constante alumno en el tipo de persona para este DF
alumnosDF["tipopersona"] = "alumno"

cursos_profesoresDF = pd.read_csv("cursos_profesores.csv")

personasDF = pd.concat([profesoresDF, alumnosDF])

lista_personas = []
lista_errores_personas = []

for index, fila in personasDF.iterrows():
    lista_personas.append({**fila})

for fila in lista_personas:
    session_mysql.begin()
    try:
        # Se procesa la dirección de la persona, insertando si corresponde los items faltantes
        pais = session_mysql.query(Pais).filter(
            Pais.nombre == fila['country']).first()
        if pais == None:
            pais = Pais(nombre=fila['country'])
            session_mysql.add(pais)

        ciudad = session_mysql.query(Ciudad).filter(
            Ciudad.nombre == fila['city']).first()
        if ciudad == None:
            ciudad = Ciudad(nombre=fila['city'])
            session_mysql.add(ciudad)

        barrio = session_mysql.query(Barrio).filter(
            Barrio.nombre == fila['town']).first()
        if barrio == None:
            barrio = Barrio(nombre=fila['town'])
            session_mysql.add(barrio)

        provincia = session_mysql.query(Provincia).filter(
            Provincia.nombre == fila['state']).first()
        if provincia == None:
            provincia = Provincia(nombre=fila['state'])
            session_mysql.add(provincia)

        lugar = session_mysql.query(Lugar).filter(and_(
            Lugar.pais == pais, Lugar.barrio == barrio, Lugar.provincia == provincia, Lugar.ciudad == ciudad)).first()
        if lugar == None:
            lugar = Lugar(pais=pais, barrio=barrio,
                          provincia=provincia, ciudad=ciudad)
            session_mysql.add(lugar)
        # ************************************************************************************************

        genero = session_mysql.query(Genero).filter(
            Genero.nombre == fila['gender']).first()
        if genero == None:
            genero = Genero(nombre=fila['gender'])
            session_mysql.add(genero)

        tipopersona = session_mysql.query(TipoPersona).filter(
            TipoPersona.nombre == fila['tipopersona']).first()
        if tipopersona == None:
            tipopersona = TipoPersona(nombre=fila['tipopersona'])
            session_mysql.add(tipopersona)

        # La persona se inserta al final porque se necesitan las entidades de genero, tipopersona y lugar ya cargadas
        persona = session_mysql.query(Persona).filter(
            Persona.personal_id == fila['personal_id']).first()
        if persona == None:
            persona = Persona(nombre=fila['first_name'], apellido=fila['last_name'], email=fila['email'], birthdate=fila['birthdate'], personal_id=fila['personal_id'],
                              lugar=lugar, genero=genero)
            session_mysql.add(persona)

        session_mysql.commit()
    except:
        session_mysql.rollback()
        lista_errores_personas.append(fila)


lista_cursos = []
lista_errores_cursos_profesores = []

for index, fila_cursos in cursos_profesoresDF.iterrows():
    lista_cursos.append({**fila_cursos})

for fila_curso in lista_cursos:
    session_mysql.begin()
    try:
        programa = session_mysql.query(Programa).filter(
            Programa.nombre == fila_curso['program']).first()
        if programa == None:
            programa = Programa(nombre=fila_curso['nombre'])
            session_mysql.add(programa)

        facultad = session_mysql.query(Facultad).filter(
            Facultad.nombre == fila_curso['branch']).first()
        if facultad == None:
            facultad = Facultad(nombre=fila_curso['branch'])
            session_mysql.add(facultad)

        universidad = session_mysql.query(Universidad).filter(
            Universidad.nombre == fila_curso['institute']).first()
        if universidad == None:
            universidad = Universidad(nombre=fila_curso['institute'])
            session_mysql.add(universidad)

        campus = session_mysql.query(Campus).filter(
            Campus.nombre == fila_curso['campus']).first()
        if campus == None:
            campus = Campus(nombre=fila_curso['campus'])
            session_mysql.add(campus)

        carrera = session_mysql.query(Carrera).filter(Carrera.programa == programa, Carrera.facultad ==
                                                      facultad, Carrera.universidad == universidad, Carrera.campus == campus).first()
        if carrera == None:
            carrera = Carrera(programa=programa, facultad=facultad,
                              universidad=universidad, campus=campus)
            session_mysql.add(carrera)

        rol = session_mysql.query(TipoPersona).filter(
            TipoPersona.nombre == 'Profesor').first()
        persona = session_mysql.query(Persona).filter(
            Persona.personal_id == fila_curso['instructor']).first()

        persona_carrera = session_mysql.query(PersonasCarreras).filter(and_(
            PersonasCarreras.persona == persona, PersonasCarreras.carrera == carrera, PersonasCarreras.tipopersona == rol)).first()
        if persona_carrera == None:
            persona_carrera = PersonasCarreras(
                persona=persona, carrera=carrera, tipopersona=rol)
            session_mysql.add(persona_carrera)

        session_mysql.commit()
    except:
        session_mysql.rollback()
        lista_errores_cursos_profesores.append(fila_curso)

lista_alumnos = []
lista_errores_cursos_alumnos = []


for index, fila_cursos in alumnosDF.iterrows():
    lista_alumnos.append({**fila_cursos})

for fila_alumnos in lista_alumnos:
    session_mysql.begin()
    try:
        persona = session_mysql.query(Persona).filter(
            Persona.personal_id == fila_alumnos['personal_id']).first()
        programa = session_mysql.query(Programa).filter(
            Programa.nombre == fila_alumnos['program']).first()
        carrera = session_mysql.query(Carrera).filter(
            Carrera.programa == programa).first()
        rol = session_mysql.query(TipoPersona).filter(
            TipoPersona.nombre == 'Alumnos').first()
        persona_carrera = session_mysql.query(PersonasCarreras).filter(and_(
            PersonasCarreras.persona == persona, PersonasCarreras.carrera == carrera, PersonasCarreras.tipopersona == rol)).first()
        if persona_carrera == None:
            persona_carrera = PersonasCarreras(
                persona=persona, carrera=carrera, tipopersona=rol)
            session_mysql.add(persona_carrera)

        session_mysql.commit()
    except:
        session_mysql.rollback()
        lista_errores_cursos_profesores.append(fila_alumnos)

session_mysql.close()
engine_mysql.dispose()
