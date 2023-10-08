import os
from decouple import config

class Settings:
    """
    Settings class

    This class is used to store the settings of the application.

    It has the following attributes:
    - DB_TYPE: This is the type of the database
    - DB_HOST: This is the hostname of the database
    - DB_PORT: This is the port of the database
    - DB_PASSWORD: This is the password of the database
    - DB_USERNAME: This is the username of the database
    - DB_NAME: This is the name of the database
    
    """
    DB_TYPE = config("DB_TYPE")
    DB_NAME = config("DB_NAME")
    DB_USER = config("DB_USER")
    DB_PASSWORD = config("DB_PASSWORD")
    DB_HOST = config("DB_HOST")
    DB_PORT = config("DB_PORT")
    LOCAL = config("LOCAL", cast=bool, default=False)
    AUTH_SERVICE_URL = config("AUTH_SERVICE_URL")


settings = Settings()
