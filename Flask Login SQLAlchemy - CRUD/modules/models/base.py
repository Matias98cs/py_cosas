from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BaseEntity(db.Model):
	__abstract__ = True

	def guardar(self):
		exito=True
		mensaje=""
		try:
			db.session.add(self)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			exito=False
			mensaje=str(e)
		return {"Resultado":None, "Exito":exito, "MensajePorFallo":mensaje}

	def borrar(self):
		exito=True
		mensaje=""
		try:
			db.session.delete(self)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			exito=False
			mensaje=str(e)
		return {"Resultado":None, "Exito":exito, "MensajePorFallo":mensaje}
		
	@classmethod
	def crear_y_obtener(cls, **kwargs):
		exito=True
		mensaje=""
		try:
			entidad = cls.query().filter_by(**kwargs).first()
			if not entidad:
				entidad = cls(**kwargs)
				db.session.add(entidad)
		except Exception as e:
			db.session.rollback()
			exito=False
			mensaje=str(e)
		return {"Resultado":entidad, "Exito":exito, "MensajePorFallo":mensaje}
	
	def serialize(self):
		serializable_data = {}
		for column in self.__table__.columns:
			serializable_data[column.name] = getattr(self, column.name)
		return serializable_data