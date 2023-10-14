from sqlalchemy.orm import Session
from fastapi import HTTPException,status, Header
from app.models import UserAssessment, Question
from app.config import settings, Permission
from requests import post
from app.fake_db_response import UserAssessments,Questions #comment it after testing and grading is done!
from app.response_schemas import AuthenticateUser
from app.models import AssessmentCategory, UserResponse, Answer, Assessment

def authenticate_user(permission: str,token: str ):
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

    request = post(
        f"{settings.AUTH_SERVICE}",
        headers={},
        data={"token": token, "permission":permission}).json()



    if request.get("status") == 401:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    if request.get("status") != 200:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
    if Permission.check_permission(request.get("user").get("permissions"), permission):

        data = {
            "id": request.get("user").get("id"),
            "permissions": request.get("user").get("permissions"),
        }

        return AuthenticateUser(**data)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="UNKNOWN PERMISSION")


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
        "id": "e2009b92-8acf-406d-a974-95fb6a5215f3",
        "permissions": ["assessment.create", "assessment.read", "assessment.update.own", "assessment.update.all", "assessment.delete.own", "assessment.delete.all"]
    }

    return AuthenticateUser(**data)
    
def check_for_assessment(assessment_id:str,db:Session):
    """
        Check for assessment:
            This function checks for assessment duration_minutes
        Parameters:
        - assessment_id : str
            assessment id of the assessment
        - db : Session
            database session


        Returns:
        - check : Assessment
            returns the Assessment object if there is a match
        - None : None
            returns None if there is no match

    """
    #validate if the assessment_id  corresponds
    check = db.query(Assessment).filter(Assessment.id==assessment_id).first()
    if not check :
        return None,HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No assessment found for provided assessment_id ")
    
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
    # #query for any questions corresponding to the assessment_id and do a join with the answers table
    questions = db.query(Question).filter(Question.assessment_id==assessment_id).all()
    if not questions:
        #for any reason if  there are no questions return false
        err_message = "No questions found under the assessment_id"
        return None, HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err_message)
    return questions, None
    
def fetch_single_assessment(skill_id:str,db:Session):
    """
        Get  single assessment :
            This function gets a single assessment details if the skill_id is present in the userAssessment database

        Parameters:
        - skill_id : str
            skill id of the user
        - db : Session
            database session


        Returns:
        - check : UserAssessment
            returns the UserAssessment object if there is a match
        - None : None
            returns None if there is no match

    """
    #query for assessment that the user has not taken
    assessment_details = db.query(Assessment).filter(Assessment.skill_id==skill_id).first()

    if not assessment_details :
        return None,HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No assessment found")
    
    return assessment_details,None

def fetch_answered_and_unanswered_questions(assessment_id:str, user_id:str,db:Session):
    """
        Fetch answered and unanswered questions:
            This function fetches the answered and unanswered questions under the assessment_id

        Parameters:
        - assessment_id : str
            assessment id of the assessment
        - user_id : str
            user id of the user
        - db : Session
            database session

        Returns:
        - answered_questions : list
            returns the list of answered questions under the assessment_id

        - questions : list
            returns the list of unanswered questions under the assessment_id
        
        - None : None
            returns None if there is no match
        
        - HTTPException : HTTPException
            returns HTTPException if there is no match
    """
    #query for any questions corresponding to the assessment_id
    questions = db.query(Question).filter(Question.assessment_id==assessment_id).all()
    if not questions:
        #for any reason if  there are no questions return false
        err_message = "No questions found under the assessment_id"
        return None, None,HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err_message)
    
    #query for any questions corresponding to the assessment_id
    user_assement_instance = db.query(UserAssessment).filter(UserAssessment.assessment_id==assessment_id, UserAssessment.user_id==user_id).first()
    if not user_assement_instance:
        #for any reason if  there are no questions return false
        err_message = "No questions found under the assessment_id"
        return None, None,HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err_message)
    
    answered_questions = db.query(UserResponse).filter(UserResponse.user_assessment_id==user_assement_instance.id).all()

    if answered_questions != []:
        for q in answered_questions:
            for question in questions:
                if q.question_id == question.id:
                    questions.remove(question)

    return questions, answered_questions, None
        