from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException,status
from app.models import UserAssessment, Question, Answer
from app.config import settings
from app.schemas import AssessmentAnswers
from app.fake_db_response import UserAssessments, Questions


def get_assessment_results(user_id: str, assessment_id: int, db : Session):

    """
    Get assessment results:
        This function gets the assessment results of a user

    Parameters:
    - user_id : str
        user id of the user
    - assessment_id : str
        assessment id of the assessment
    - db : Session
        database session

    Returns:
    - score : float
        score of the user
    - status : str
        status of the user
    - db_questions : List[Question]
        list of questions in the assessment
        
    """
    
    # query = db.query(UserAssessment)\
    #     .filter(
    #         and_(UserAssessment.user_id==user_id, UserAssessment.assessment_id==assessment_id)\
    #         )
    
    # assessment = query.first()

    # if not query:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Assessment with id {assessment_id} not found",
    #     )
    
    # score = assessment.score
    # status = assessment.status

    # db_questions = db.query(Question).join(Answer, Question.id == Answer.question_id)\
    #                 .filter(Question.assessment_id == assessment_id).all()
    
    print(user_id, assessment_id)
    assessment_obj = None

    for assessment in UserAssessments:
        print(assessment.get('assessment_id'))
        if assessment['assessment_id'] == assessment_id:
            assessment_obj = assessment
        else:
            continue
    
    print(assessment_obj)
    if assessment_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assessment with id {assessment_id} not found",
        )
    
    score = assessment_obj.get('score')
    assessment_status = assessment_obj.get('status')   

    db_questions = [question for question in Questions if question['assessment_id'] == assessment_id]

    return score, assessment_status, db_questions