# database.py
from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings


def get_db_engine():
    """
        Get db engine:
            This function returns the database engine based on the database type.
            If the database type is sqlite then it returns the sqlite engine else it returns the postgresql engine.
            it also checks if the database type is sqlite then it checks if the database is present or not.
            If the database is not present then it creates the database.
            It's parameters are taken from the config.py file which is gotten from the environment variables.

        Parameters:
        - DB_TYPE: This is the type of the database used (sqlite, postgresql). 
        - DB_NAME: This is the name of the database. 
        - DB_USER: This is the username of the database. 
        - DB_PASSWORD: This is the password of the database. 
        - DB_HOST: This is the hostname of the database.
        - DB_PORT: This is the port of the database.

            """
    DB_TYPE = settings.DB_TYPE
    DB_NAME = settings.DB_NAME
    DB_USER = settings.DB_USER
    DB_PASSWORD = settings.DB_PASSWORD
    DB_HOST = settings.DB_HOST
    DB_PORT = settings.DB_PORT

    DATABASE_URL = "sqlite:///./database.db"

    if DB_TYPE == "postgresql":
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        
    else:
        DATABASE_URL = "sqlite:///./database.db"

    if DB_TYPE == "sqlite":
        db_engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    else:
        db_engine = create_engine(DATABASE_URL)

    return db_engine


db_engine = get_db_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

Base = declarative_base()


def create_database():
    """
        Create database:
            This function creates the database if it is not present and 
            creates all the tables in the database. It returns the database engine.

            This function is called in the main.py file. If a LOCAL environment variable is set to True
    """
    print("Connected to the database")
    return Base.metadata.create_all(bind=db_engine)


def get_db():
    """
        Get db:
            This function returns the database session.
            It is used in the in any router file to get the database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    return db

def get_db_unyield():
    """
        Get db unyield:
            This function returns the database session.
            It is used mainly for writing to the database externally
            from the entire application.
    """
    create_database()
    db = SessionLocal()
    return db
