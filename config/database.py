import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

base_dir = os.path.dirname(os.path.realpath(__file__))

database_url = os.getenv("DATABASE_URL")

engine = create_engine(database_url, echo=True) # para podruccion debe de estar en echo = false

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()