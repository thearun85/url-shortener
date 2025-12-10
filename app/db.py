from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

class Base(DeclarativeBase):
    pass

engine = None
Session = None

def init_db(db_url):
    global engine, Session
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)

def get_session():
    if Session is None:
        raise RuntimeError("Database is not initialized yet. Call init_db.")
    return Session()
