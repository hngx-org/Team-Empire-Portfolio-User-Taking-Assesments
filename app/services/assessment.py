from pprint import pprint
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException,status
from app.models import UserAssessment, Question, Answer, User
from app.config import settings
from app.schemas import AssessmentAnswers
from app.fake_db_response import UserAssessments, Questions, Answers


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
        status of the assessment
    - db_questions : List[Question]
        list of questions in the assessment

    """

    valid_user = db.query(User).filter(User.id == user_id).first()

    if not valid_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    query = db.query(UserAssessment)\
        .filter(
            and_(UserAssessment.user_id==user_id, UserAssessment.assessment_id==assessment_id)\
            )

    assessment = query.first()

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assessment with id {assessment_id} not found",
        )

    score = assessment.score
    assessment_status = assessment.status

    db_questions = db.query(Question).join(Answer, Question.id == Answer.question_id)\
                    .filter(Question.assessment_id == assessment_id).all()


    questions_with_answers = []
    for item in db_questions:
        var = {}
        question = item.__dict__
        var['question_text'] = question['question_text']

        answer = question['answer'].__dict__
        var['answer_text'] = answer['correct_option']

        questions_with_answers.append(var)


    if score is None and assessment_status is None and not questions_with_answers:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting results for {assessment_id}",
        )
    # assessment_obj = None

    # for assessment in UserAssessments:

    #     if assessment['assessment_id'] == assessment_id:
    #         assessment_obj = assessment
    #     else:
    #         continue


    # if assessment_obj is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Assessment with id {assessment_id} not found",
    #     )

    # score = assessment_obj.get('score')
    # assessment_status = assessment_obj.get('status')

    # db_questions = [question for question in Questions if question['assessment_id'] == assessment_id]
    # for question in db_questions:
    #     question['answer_text'] = ''
    #     for answer in Answers:
    #         if answer['question_id'] == question['id']:
    #             question['answer_text'] = answer['answer_text']
    #         else:
    #             continue

    return score, assessment_status, questions_with_answers

def get_completed_assessments(user_id,db:Session):
    completed_assessments=db.query(UserAssessment).filter(UserAssessment.user_id==user_id,UserAssessment.status=='complete').all()
    if completed_assessments==[]:
        return None,HTTPException(status_code=404,detail="no assessment found")

    response=[]
    for assessment in completed_assessments:
        response.append(
            {
                "id": assessment.id,
                "user_id": assessment.user_id,
                "assessment_id":assessment.assessment_id,
                "assessment_name":assessment.assessment.title if assessment.assessment else None,
                "skill_id":assessment.user_badge[0].skill_badge.skill_id if assessment.user_badge else None,
                "score":assessment.score,
                "status": assessment.status,
                "submission_date": assessment.submission_date,
                "badge_id":assessment.user_badge[0].id if assessment.user_badge else None,
                "badge_name":assessment.user_badge[0].skill_badge.name if assessment.user_badge else None,


            }
        )
    return response,None


