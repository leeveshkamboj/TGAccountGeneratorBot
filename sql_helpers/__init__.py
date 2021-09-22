import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


DB_URI = os.environ.get("DATABASE_URL", None).replace('postgres://', 'postgresql://')


def start() -> scoped_session:
    engine = create_engine(DB_URI)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()
