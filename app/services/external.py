from sqlalchemy.orm import Session
from fastapi import HTTPException,status, Header
from app.models import UserAssessment, Question
from app.config import settings, Permission
from requests import get
from app.fake_db_response import UserAssessments,Questions #comment it after testing and grading is done!
from app.response_schemas import AuthenticateUser


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
    request = get(f"{settings.AUTH_SERVICE_URL}", headers={"Authorization": token})

    if request.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    if request.json()["permissions"]["assessment"] == []:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    
    if Permission.check_permissions(request.json()["permissions"]["assessment"]) == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    
    request = request.json()

    data = {
        "user_id": request["user_id"],
        "is_super_admin": request["is_super_admin"],
        "permissions": request["permissions"]["assessment"]
    }

    return AuthenticateUser(**data)


# create a function that has a fixed token for testing
def fake_authenticate_user(fake_token: str ="l3h5.34jb3,4mh346gv,34h63vk3j4h5k43hjg54kjhkg4j6h45g6kjh45gk6jh6k6g34hj6"):
    """
    ***fake_authenticate_user(SUBJECT TO CHANGE when authentication service provides us with information)***
    Takes the fake_token from the header and makes a request to the authentication service to authenticate the user.

    Parameters:
    - fake_token: This is the fake_token of the user gotten from the header.

    Returns:
    - data: This is the data gotten from the authentication service.

    Raises:
    - HTTPException: This is raised if the authentication service returns a status code other than 200.
    
    """
    if fake_token != "l3h5.34jb3,4mh346gv,34h63vk3j4h5k43hjg54kjhkg4j6h45g6kjh45gk6jh6k6g34hj6":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    data = {
        "user_id": "2mn3m4n23mb34n23b4234234nbm234",
        "is_super_admin": False,
        "permissions": ['assessments::view', 'assessment::take','results::view',]
    }

    return AuthenticateUser(**data)
    

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
    #uncomment the lines below after grading is done!
    '''
    check = db.query(UserAssessment).filter(UserAssessment.user_id==user_id,UserAssessment.assessment_id==assessment_id).first()

    if not check :
        return None,HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="There is no match for user_id or assessment_id")
    
    return check,None
    '''
    #comment the lines below after grading is done!
    check = [assessment for assessment in UserAssessments if assessment['user_id'] == user_id and assessment['assessment_id'] == assessment_id]
    if len(check) == 0:
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
    #uncomment the lines below after grading is done!
    '''
    questions = db.query(Question).filter(Question.assessment_id==assessment_id).all()
    if not questions:
        #for any reason if  there are no questions return false
        err_message = "No questions found under the assessment_id"
        return None,HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err_message)
    return questions,None
    '''
    #comment the lines below after grading is done!
    questions = [question for question in Questions if  question['assessment_id'] == assessment_id]
    if len(questions) == 0:
        return None,HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No questions found under the assessment_id")
    return questions,None