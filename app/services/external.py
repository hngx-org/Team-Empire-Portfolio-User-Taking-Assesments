from sqlalchemy.orm import Session
from fastapi import HTTPException,status, Header
from app.models import UserAssessment, Question
from app.config import settings
from requests import get

err_message = ""

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

def check_for_assessment(user_id:str,assessment_id:str,db:Session):
    """
        Check for assessment:
            This function checks if the user_id and assessment_id are present in the database

        Parameters:
        - user_id : str
            user id of the user
        - assessment_id : str
            assessment id of the assessment
        - db : Session
            database session

        Returns:
        - check : UserAssessment
            returns the UserAssessment object if there is a match
        - None : None
            returns None if there is no match

    """
    check = db.query(UserAssessment).filter(UserAssessment.user_id==user_id,UserAssessment.assessment_id==assessment_id).first()

    if not check :
        return None,HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="There is no match for user_id or assessment_id")
    
    return check,None


def fetch_questions(assessment_id:str,db:Session):
    """
        Fetch questions:
            This function fetches the questions under the assessment_id

        Parameters:
        - assessment_id : str
            assessment id of the assessment
        - db : Session
            database session

        Returns:
        - check : bool
            returns True if there are questions under the assessment_id
        - questions : list
            returns the list of questions under the assessment_id

    """
    questions = db.query(Question).filter(Question.assessment_id==assessment_id).all()
    if not questions:
        #for any reason if  there are no questions return false
        err_message = "No questions found under the assessment_id"
        return None,HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err_message)
    return questions,None