import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}/{}".format(os.environ.get('POSTGRES_USER'),
                                                            os.environ.get('POSTGRES_PASSWORD'),
                                                            os.environ.get('POSTGRES_SERVER'),
                                                            os.environ.get('POSTGRES_DATABASE'))

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
