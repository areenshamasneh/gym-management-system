from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from decouple import config

DATABASE_URL = config('DATABASE_URL')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    try:
        with engine.connect() as connection:
            print("Database connection successful.")
    except Exception as e:
        print(f"Database connection error: {e}")
