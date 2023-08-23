from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import db_connector, db_user, db_password, db_ip_address, db_name

Base = declarative_base()

def _crear_conexion():
    url = f"{db_connector}://{db_user}:{db_password}@{db_ip_address}/{db_name}"
    try:
        engine = create_engine(url, echo=False)
        if not database_exists(engine.url):
            create_database(engine.url)
        else:
            pass
        return engine
    except:
        print(f"Error al crear conector {db_connector}, servidor: {db_ip_address}")
        return None

def obtener_session():
    engine = _crear_conexion()
    Base.metadata.create_all(engine)
    if engine:
        Session = sessionmaker(bind=engine)
        return Session()
    return None