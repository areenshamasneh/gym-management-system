import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from gym_management.settings import DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=True)

SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(SessionFactory)

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
