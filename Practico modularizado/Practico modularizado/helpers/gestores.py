class comun():
    @classmethod
    def crear_y_obtener(cls, session, **kwargs):
        entidad = session.query(cls).filter_by(**kwargs).first()
        if not entidad:
            entidad = cls(**kwargs)
            session.add(entidad)
        return entidad

	@classmethod
    def obtenerId(cls, session, id):
        entidad = session.query(cls).filter_by(cls.id==id).first()
        return entidad
