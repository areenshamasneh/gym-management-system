from sqlalchemy import create_engine # type: ignore
from sqlalchemy.orm import sessionmaker, scoped_session # type: ignore

from common.threads.thread import get_request_id
from gym_management.settings import DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=True)

SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

Session = scoped_session(SessionFactory, scopefunc=get_request_id)

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
