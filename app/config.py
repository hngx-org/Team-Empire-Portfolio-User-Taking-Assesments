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
    AUTH_SERVICE = config("AUTH_SERVICE")
    MESSAGING=config("MESSAGING")
    ENVIRONMENT = config("ENVIRONMENT", default="development")
    FRONTEND_URL = config("FRONTEND_URL") 
    BADGE_SERVICE= config("BADGE_SERVICE")



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

        return permission in permission_list

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
Permission = Permissions(permissions=["assessment.create", "assessment.read", "assessment.update.own", "assessment.update.all", "assessment.delete.own", "assessment.delete.all"])
