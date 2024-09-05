import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from common.threads.thread import get_local
from gym_management.settings import DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=True)

SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

Session = scoped_session(SessionFactory, scopefunc=lambda: get_local('request_id'))

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
