import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from gym_management.settings import DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
