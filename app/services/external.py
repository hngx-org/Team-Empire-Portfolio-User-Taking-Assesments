from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException,status, Header
from app.models import UserAssessment, Question, Answer
from app.config import settings
from app.schemas import AssessmentAnswers
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


def get_assessment_results(user_id, assessment_id, db : Session):
    
    query = db.query(UserAssessment)\
        .filter(
            and_(UserAssessment.user_id==user_id, UserAssessment.assessment_id==assessment_id)\
            )
    
    assessment = query.first()

    if not query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assessment with id {assessment_id} not found",
        )
    
    score = assessment.score
    status = assessment.status

    db_questions = db.query(Question).join(Answer, Question.id == Answer.question_id)\
                    .filter(Question.assessment_id == assessment_id).all()
    
    return score, status, db_questions
