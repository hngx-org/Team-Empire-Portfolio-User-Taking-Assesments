from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException,status, Header
from app.models import UserAssessment, Question, Answer
from app.config import settings
from app.schemas import AssessmentAnswers


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