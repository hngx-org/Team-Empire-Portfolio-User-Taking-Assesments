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
    ENVIRONMENT = config("ENVIRONMENT", default="development")

# a class that takes in a list of permissions and checks if a permission is present in the list
class Permissions():
    """
    Permissions class

    This class is used to check if a permission is present in the list of permissions.

    It has the following attributes:
    - permissions: This is the list of permissions

    It has the following methods:
    - check_permission: This method checks if a permission is present in the list of permissions

    """
    def __init__(self, permissions):
        self.permissions = permissions

    def check_permission(self, permission_list, permission):
        
        """
        Check permission:
            This method checks if a permission is present in the list of permissions

        Parameters:
        - permission: This is the permission to be checked

        Returns:
        - bool: This is True if the permission is present in the list of permissions else False

        """
        
        if permission in permission_list:
            return True
        return False
    
    def check_permissions(self, permission_list):
        """
        Check permissions:
            This method checks if a list of permissions is present in the list of permissions

        Parameters:
        - permission_list: This is the list of permissions to be checked

        Returns:
        - bool: This is True if the list of permissions is present in the list of permissions else False

        """
        return all(self.check_permission(permission_list, permission) for permission in self.permissions)
  

settings = Settings()
Permission = Permissions(permissions=['assessments::view', 'assessment::take', 'results::view', 'assessments::start'])