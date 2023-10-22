from sqlalchemy.orm import Session
from fastapi import HTTPException,status, Header
from app.models import UserAssessment, Question
from app.config import settings, Permission
from requests import post
from app.fake_db_response import UserAssessments,Questions #comment it after testing and grading is done!
from app.response_schemas import AuthenticateUser
from app.models import AssessmentCategory, UserResponse, Answer, Assessment
from app.response_schemas import Questions

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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
                "message": "Unauthorized",
                "status_code": status.HTTP_401_UNAUTHORIZED,
                "data":{}
            })

    if request.get("status") != 200:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                "message": "unable to authenticate user",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data":{}
            })

    if Permission.check_permission(request.get("user").get("permissions"), permission):

        data = {
            "id": request.get("user").get("id"),
            "permissions": request.get("user").get("permissions"),
        }

        return AuthenticateUser(**data)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
        "message": "Unknow permission",
        "status_code": status.HTTP_400_BAD_REQUEST,
        "data":{}
        }
    )


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

def fetch_assessment_questions(user_id, assessment_id: str, count: bool, db: Session):
    """
        Fetch assessment questions:
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
    # query for any questions corresponding to the assessment_id and do a join with the answers table
    query = (
        db.query(Question)
        .filter(Question.assessment_id == assessment_id)
    )

    if count:
        return query.count(), None

    questions = [
        Questions(
            question_id=question.id,
            question_no=question.question_no or 0,
            question_text=question.question_text,
            question_type=question.question_type,
            answer_id=question.answer.id,
            options=question.answer.options,
        )
        for question in query.all()
    ]

    is_user_assessment = (
        db.query(UserAssessment)
        .filter(
            UserAssessment.user_id == user_id,
            UserAssessment.assessment_id == assessment_id,
            UserAssessment.status == "pending",
        )
        .first()
    )

    if not is_user_assessment:
        user_assessment = UserAssessment(
            user_id=user_id,
            assessment_id=assessment_id,
            score=0,
            status="pending",
            time_spent=0,
            submission_date=None,
        )
        db.add(user_assessment)
        db.commit()
        db.refresh(user_assessment)

    if not questions:
        return None, HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "No questions found under the assessment_id",
                "status_code": status.HTTP_404_NOT_FOUND,
                "data": {},
            },
        )

    return questions, None


def fetch_single_assessment( assessment_id: int, db: Session):
    """
    Fetch assessment:
        This function fetches the assessment details

    Parameters:
    - skill_id : str
        skill id of the assessment
    - assessment_id : str
        assessment id of the assessment
    - db : Session
        database session

    Returns:
    - assessment_details : dict
        Dictionary containing the assessment details
    """
    assessment = (
        db.query(Assessment)
        .filter(Assessment.id == assessment_id)
        .first()
    )

    if not assessment:
        return None, HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                "message": "No assessment found",
                "status_code": status.HTTP_404_NOT_FOUND,
                "data":{}
            })

    question_count = (
        db.query(Question)
        .filter(Question.assessment_id == assessment.id)
        .count()
    )

    assessment_details = {
        "assessment_id": assessment.id,
        "skill_id": assessment.skill_id,
        "title": assessment.title,
        "description": assessment.description,
        "duration_minutes": assessment.duration_minutes,
        "question_count": question_count,
        "status": assessment.status,
        "start_date": assessment.start_date,
        "end_date": assessment.end_date,
    }

    return assessment_details, None

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
    user_assement_instance = db.query(UserAssessment).filter(UserAssessment.assessment_id==assessment_id, UserAssessment.user_id==user_id, UserAssessment.status == "pending").first()
    if not user_assement_instance:
        #for any reason if  there are no questions return false
        err_message = "No questions found under the assessment_id"
        return None, None,HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                "message": err_message,
                "status_code": status.HTTP_404_NOT_FOUND,
                "data":{}
            })
    

    #query for any questions corresponding to the assessment_id
    questions = db.query(Question).filter(Question.assessment_id==assessment_id).all()
    if not questions:
        #for any reason if  there are no questions return false
        err_message = "No questions found under the assessment_id"
        return None, None,HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                "message": err_message,
                "status_code": status.HTTP_404_NOT_FOUND,
                "data":{}
            })


    answered_questions = db.query(UserResponse).filter(UserResponse.user_assessment_id==user_assement_instance.id)
    if answered_questions != []:
        for q_ans in answered_questions.all():
            for q in questions:
                if q_ans.question_id == q.id:
                    questions.remove(q)
            
                    
    return questions, answered_questions, None
