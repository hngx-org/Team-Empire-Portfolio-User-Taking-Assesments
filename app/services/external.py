from sqlalchemy.orm import Session
from fastapi import HTTPException,status, Header
from app.models import UserAssessment, Question
from app.config import settings
from requests import get

def authenticate_user(token: str = Header(...)):
    """
    ***authenticate_user(SUBJECT TO CHANGE)***
    Takes the token from the header and makes a request to the authentication service to authenticate the user.

    Parameters:
    - token: This is the token of the user gotten from the header.

    Returns:
    - data: This is the data gotten from the authentication service.

    Raises:
    - HTTPException: This is raised if the authentication service returns a status code other than 200.
    """
    request = get(f"{settings.AUTH_SERVICE_URL}/api/auth/verify", headers={"Authorization": token})

    if request.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    request = request.json()

    data = {
        "user_id": request["user_id"],
        "is_super_admin": request["is_super_admin"],
        "permissions": request["permissions"]["assessment"]
    }

    return data

