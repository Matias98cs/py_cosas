from sqlalchemy import Column, Integer, String, ForeignKey, Date, case, UniqueConstraint, func
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import date

Base = declarative_base()


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
    # tipo_id = Column(Integer, ForeignKey("tipopersona.id"))

    genero = relationship("Genero", backref="related_genero")
    lugar = relationship("Lugar", backref="related_lugar")
    # tipopersona = relationship("TipoPersona", backref="related_tipopersona")

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


class PersonasCarreras(Base):
    __tablename__ = "personasCarreras"
    __table_args__ = (UniqueConstraint('persona_id', 'carrera_id',
                      'tipo_id', name='uix_pers_carreras_tipo_unico'),)
    id = Column(Integer, primary_key=True)
    persona_id = Column(Integer, ForeignKey("personas.id"))
    carrera_id = Column(Integer, ForeignKey("carrera.id"))
    tipo_id = Column(Integer, ForeignKey("tipopersona.id"))

    persona = relationship("Persona", backref="related_persona")
    carrera = relationship("Carrera", backref="related_carrera")
    tipopersona = relationship("TipoPersona", backref="related_tipopersona")
