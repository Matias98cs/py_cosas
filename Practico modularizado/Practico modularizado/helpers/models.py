
from sqlalchemy import Column, Integer, String, Date, ForeignKey, case, UniqueConstraint, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
import datetime
from .database import Base
from .gestores import comun 

class Persona(Base, comun):
	__tablename__ = "personas"
	id = Column(Integer, primary_key = True)
	nombre = Column(String(100))
	apellido = Column(String(100))
	email = email = Column(String(255), unique = True)
	birthdate = Column(Date)
	personal_id = Column(String(50), unique = True)
	genero_id = Column(Integer,ForeignKey("genero.id"), nullable=False)
	lugar_id = Column(Integer, ForeignKey("lugar.id"), nullable=False)

	genero = relationship("Genero", backref = "related_genero")
	lugar = relationship("Lugar", backref = "related_lugar")

	def __init__(self, nombre, apellido, email, birthdate, personal_id, genero, lugar):
		self.nombre = nombre
		self.apellido = apellido
		self.email = email
		self.birthdate = birthdate
		self.personal_id = personal_id
		self.genero = genero
		self.lugar = lugar

	@hybrid_property
	def age(self):
		today = datetime.date.today()
		edad = today.year - self.birthdate.year
		if (today.month, today.day) > (self.birthdate.month, self.birthdate.day):
			edad -= 1
		return edad

	@age.expression
	def age(cls):
		today = datetime.date.today()
		birthdate_year = func.extract('year', cls.birthdate)
		birthdate_month = func.extract('month', cls.birthdate)
		birthdate_day = func.extract('day', cls.birthdate)
		return case(
			(
				(
					(birthdate_month < today.month) |
					((birthdate_month == today.month) & (birthdate_day <= today.day)),
					today.year - birthdate_year - 1
				)
			),
			else_=today.year - birthdate_year
		)

class Genero(Base, comun):
	__tablename__ = "genero"
	id = Column(Integer, primary_key = True)
	nombre = Column(String(50), unique = True)

	def __init__(self, nombre):
		self.nombre = nombre

class TipoPersona(Base, comun):
	__tablename__ = "tipopersona"
	id = Column(Integer, primary_key = True)
	nombre = Column(String(50), unique = True)

	def __init__(self, nombre):
		self.nombre = nombre

class Pais(Base, comun):
	__tablename__ = "pais"
	id = Column(Integer, primary_key = True)
	nombre = Column(String(100), unique = True)

	def __init__(self, nombre):
		self.nombre = nombre

class Ciudad(Base, comun):
	__tablename__ = "ciudad"
	id = Column(Integer, primary_key = True)
	nombre = Column(String(100), unique = True)

	def __init__(self, nombre):
		self.nombre = nombre

class Barrio(Base, comun):
	__tablename__ = "barrio"
	id = Column(Integer, primary_key = True)
	nombre = Column(String(100), unique = True)

	def __init__(self, nombre):
		self.nombre = nombre

class Provincia(Base, comun):
	__tablename__ = "provincia"
	id = Column(Integer, primary_key = True)
	nombre = Column(String(100), unique = True)

	def __init__(self, nombre):
		self.nombre = nombre

class Lugar(Base, comun):
	__tablename__ = "lugar"
	__table_args__ = (UniqueConstraint('pais_id','ciudad_id','barrio_id','provincia_id', name='uidx_sitio_unico'), )
	id = Column(Integer, primary_key = True)
	pais_id = Column(Integer, ForeignKey("pais.id"), nullable=False)
	ciudad_id = Column(Integer,ForeignKey("ciudad.id"), nullable=False)
	barrio_id = Column(Integer,ForeignKey("barrio.id"), nullable=False)
	provincia_id = Column(Integer,ForeignKey("provincia.id"), nullable=False)

	pais = relationship("Pais", backref = "related_pais")
	ciudad = relationship("Ciudad", backref = "related_ciudad")
	barrio = relationship("Barrio", backref = "related_barrio")
	provincia = relationship("Provincia", backref = "related_provincia")

	def __init__(self, pais, ciudad, barrio, provincia):
		self.pais = pais
		self.ciudad = ciudad
		self.barrio = barrio
		self.provincia = provincia

class Programa(Base, comun):
	__tablename__ = "programa"
	id = Column(Integer, primary_key = True)	
	nombre = Column(String(100), unique = True)

	def __init__(self, nombre):
		self.nombre = nombre

class Facultad(Base, comun):
	__tablename__ = "facultad"
	id = Column(Integer, primary_key = True)	
	nombre = Column(String(100), unique = True)

	def __init__(self, nombre):
		self.nombre = nombre

class Universidad(Base, comun):
	__tablename__ = "universidad"
	id = Column(Integer, primary_key = True)	
	nombre = Column(String(100), unique = True)

	def __init__(self, nombre):
		self.nombre = nombre

class Campus(Base, comun):
	__tablename__ = "campus"
	id = Column(Integer, primary_key = True)	
	nombre = Column(String(100), unique = True)

	def __init__(self, nombre):
		self.nombre = nombre

class Carrera(Base, comun):
	__tablename__ = "carrera"
	__table_args__ = (UniqueConstraint('programa_id', 'facultad_id', 'universidad_id','campus_id', name='uix_table_programa_facultad_universidad_campus'),)
	id = Column(Integer, primary_key = True)
	programa_id = Column(Integer, ForeignKey("programa.id"), nullable=False)
	facultad_id = Column(Integer, ForeignKey("facultad.id"), nullable=False)
	universidad_id = Column(Integer, ForeignKey("universidad.id"), nullable=False)
	campus_id = Column(Integer, ForeignKey("campus.id"), nullable=False)

	programa = relationship("Programa", backref = "related_programa")
	facultad = relationship("Facultad", backref = "related_facultad")
	universidad = relationship("Universidad", backref = "related_universidad")
	campus = relationship("Campus", backref = "related_campus")

	def __init__(self, programa, facultad, universidad, campus):
		self.programa = programa
		self.facultad = facultad
		self.universidad = universidad
		self.campus = campus

class personasCarreras(Base, comun):
	__tablename__ = "personasCarreras"
	__table_args__ = (UniqueConstraint('persona_id', 'carrera_id', 'tipo_id', name='uix_pers_carreras_tipo_unico'),)
	id = Column(Integer, primary_key = True)
	persona_id = Column(Integer, ForeignKey("personas.id"), nullable=False)
	carrera_id = Column(Integer, ForeignKey("carrera.id"), nullable=False)
	tipo_id = Column(Integer, ForeignKey("tipopersona.id"), nullable=False)

	persona = relationship("Persona", backref = "related_persona")
	carrera = relationship("Carrera", backref = "related_carrera")
	tipopersona = relationship("TipoPersona", backref = "related_tipopersona")

	def __init__(self, persona, carrera, tipopersona):
		self.persona = persona
		self.carrera = carrera
		self.tipopersona = tipopersona



