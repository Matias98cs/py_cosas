import pandas
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Date, ForeignKey, case, and_, or_, extract, UniqueConstraint, func
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import relationship, sessionmaker, column_property, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import date
import pandas as pd

Base = declarative_base()


def crear_conexion(db_connector, db_user, db_password, db_ip_address, db_name):
    # print(f"mysql+pymysql:://{db_user}:{db_password}@localhost/{db_name}")
    # url = f"{db_connector}://{db_user}:{db_password}@{db_ip_address}/{db_name}"
    url = f"mysql+pymysql://{db_user}:{db_password}@{db_ip_address}/{db_name}"
    try:
        engine = create_engine(url, echo=False)
        if not database_exists(engine.url):
            create_database(engine.url)
        else:
            pass
        return engine
    except:
        print(
            f"Error al crear conector {db_connector}, servidor: {db_ip_address}")
        return None


def obtener_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()


class Persona(Base):
    __tablename__ = "personas"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    apellido = Column(String(100))
    email = email = Column(String(255), unique=True)
    birthdate = Column(Date)
    personal_id = Column(String(50), unique=True)
    genero_id = Column(Integer, ForeignKey("genero.id"))
    lugar_id = Column(Integer, ForeignKey("lugar.id"))

    tipo_id = Column(Integer, ForeignKey("tipopersona.id"))
    tipopersona = relationship("TipoPersona", backref="related_tipopersona")

    genero = relationship("Genero", backref="related_genero")
    lugar = relationship("Lugar", backref="related_lugar")

    @hybrid_property
    def age(self):
        today = date.today()
        edad = today.year - self.birthdate.year
        if (today.month, today.day) > (self.birthdate.month, self.birthdate.day):
            edad -= 1
        return edad

    @age.expression
    def age(cls):
        today = date.today()
        birthdate_year = func.extract('year', cls.birthdate)
        birthdate_month = func.extract('month', cls.birthdate)
        birthdate_day = func.extract('day', cls.birthdate)
        return case(
            (
                (
                    (birthdate_month < today.month) |
                    ((birthdate_month == today.month)
                     & (birthdate_day <= today.day)),
                    today.year - birthdate_year - 1
                )
            ),
            else_=today.year - birthdate_year
        )


class Genero(Base):
    __tablename__ = "genero"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True)


class TipoPersona(Base):
    __tablename__ = "tipopersona"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True)


class Pais(Base):
    __tablename__ = "pais"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True)


class Ciudad(Base):
    __tablename__ = "ciudad"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True)


class Barrio(Base):
    __tablename__ = "barrio"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True)


class Provincia(Base):
    __tablename__ = "provincia"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True)


class Lugar(Base):
    __tablename__ = "lugar"
    __table_args__ = (UniqueConstraint('pais_id', 'ciudad_id',
                      'barrio_id', 'provincia_id', name='uidx_sitio_unico'), )
    id = Column(Integer, primary_key=True)
    pais_id = Column(Integer, ForeignKey("pais.id"))
    ciudad_id = Column(Integer, ForeignKey("ciudad.id"))
    barrio_id = Column(Integer, ForeignKey("barrio.id"))
    provincia_id = Column(Integer, ForeignKey("provincia.id"))

    pais = relationship("Pais", backref="related_pais")
    ciudad = relationship("Ciudad", backref="related_ciudad")
    barrio = relationship("Barrio", backref="related_barrio")
    provincia = relationship("Provincia", backref="related_provincia")


class Programa(Base):
    __tablename__ = "programa"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True)


class Facultad(Base):
    __tablename__ = "facultad"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True)


class Universidad(Base):
    __tablename__ = "universidad"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True)


class Campus(Base):
    __tablename__ = "campus"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True)

# Completar la entidad faltante de acuerdo a los datos de origen
#
#
#


class Carrera(Base):
    __tablename__ = "carrera"
    __table_args__ = (UniqueConstraint('programa_id', 'facultad_id', 'universidad_id',
                      'campus_id', name='uix_table_programa_facultad_universidad_campus'),)
    id = Column(Integer, primary_key=True)
    programa_id = Column(Integer, ForeignKey("programa.id"))
    facultad_id = Column(Integer, ForeignKey("facultad.id"))
    universidad_id = Column(Integer, ForeignKey("universidad.id"))
    campus_id = Column(Integer, ForeignKey("campus.id"))

    programa = relationship("Programa", backref="related_programa")
    facultad = relationship("Facultad", backref="related_facultad")
    universidad = relationship("Universidad", backref="related_universidad")
    campus = relationship("Campus", backref="related_campus")

# Completar la entidad que falta para relacionar alumnos y profesores con sus respectivos cursos
#
#
#


base_general = "Ejercicio_1"
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

# print(profesoresDF)
# print(alumnosDF)
# print(personasDF)

lista_personas = []
lista_errores = []

for index, fila in personasDF.iterrows():
    lista_personas.append({**fila})


# print(lista_personas[0])


# Nuevo dataframe desde la unión de los DF de profesores y alumnos

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
            persona = Persona(
                nombre=fila['first_name'], apellido=fila['last_name'], email=fila['email'],
                birthdate=fila['birthdate'], personal_id=fila['personal_id'],
                tipopersona=tipopersona, lugar=lugar, genero=genero
            )
            session_mysql.add(persona)

        session_mysql.commit()
    except:
        session_mysql.rollback()
        lista_errores.append(fila)


session_mysql.close()
engine_mysql.dispose()


persona = session_mysql.query(Persona).join(TipoPersona).join(Genero).filter(
    and_(TipoPersona.nombre == "Alumno", Genero.nombre == "Female")).first()

# persona.__dict__
# print(persona.__dict__)


tipo = session_mysql.query(TipoPersona).filter(
    TipoPersona.nombre == 'Alumno').first()
alumnos = session_mysql.query(Persona).join(TipoPersona).join(
    Genero).filter(and_(Persona.age < 40, Persona.tipopersona == tipo)).all()

# for cadaUno in alumnos:
#     print(cadaUno.nombre, cadaUno.apellido, cadaUno.email, cadaUno.genero.nombre, cadaUno.birthdate, cadaUno.lugar.pais.nombre, cadaUno.personal_id,
#           cadaUno.lugar.ciudad.nombre, cadaUno.lugar.barrio.nombre, cadaUno.lugar.provincia.nombre, cadaUno.tipopersona.nombre, cadaUno.age)


# todos = session_mysql.query(Persona).join(
#     TipoPersona).join(Genero).filter(Persona.age > 40).all()
# for cadaUno in todos:
#     print(cadaUno.nombre, cadaUno.apellido, cadaUno.email, cadaUno.genero.nombre, cadaUno.birthdate, cadaUno.lugar.pais.nombre, cadaUno.personal_id,
#           cadaUno.lugar.ciudad.nombre, cadaUno.lugar.barrio.nombre, cadaUno.lugar.provincia.nombre, cadaUno.tipopersona.nombre, cadaUno.age)


df = pandas.read_sql_query(
    sql=session_mysql.query(Persona, TipoPersona.nombre.label("TipoPersona"), Genero.nombre.label(
        "Genero"), Persona.age).join(TipoPersona).join(Genero).filter(Persona.age > 40).statement,
    con=engine_mysql
)

# Exporta a excel los datos recuperados
df.to_excel('ejemplo.xlsx')

# Muestra en consola los datos recuperados
print(df)
