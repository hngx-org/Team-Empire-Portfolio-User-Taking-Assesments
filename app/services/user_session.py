from sqlalchemy.orm import Session
from app.models import UserAssessment, Question, UserResponse, Answer, Assessment,User
from app.schemas import UserAssessmentanswer
from fastapi import HTTPException, status
from app.response_schemas import Response
import requests
import json
from app.config import settings
from fastapi import BackgroundTasks
from datetime import datetime as time

# save session details
def save_session(data: UserAssessmentanswer, user_id: int, db: Session, token: str):
    """
    Save session details:
    This function saves the session details of a user

    Parameters:
    - data : SessionData
        SessionData object
    - user_id : int
        user id of the user
    - db : Session
        database session
    - token : str
        authentication token

    Returns:
    - response : dict
        dictionary containing the response message, status code, score, badge ID, and assessment ID
    """
    user_assessment_instance = (
        db.query(UserAssessment)
        .filter(
            UserAssessment.user_id == user_id,
            UserAssessment.assessment_id == data.assessment_id,
            UserAssessment.status == "pending"
        )
        .first()
    )

    if not user_assessment_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no match for user_id or assessment_id"
        )

    if not data.is_submitted and data.time_spent is None:
        user_response_instance = (
            db.query(UserResponse)
            .filter(
                UserResponse.user_assessment_id == user_assessment_instance.id,
                UserResponse.question_id == data.response.question_id
            )
            .first()
        )

        if not user_response_instance:
            user_response_instance = UserResponse(
                user_assessment_id=user_assessment_instance.id,
                question_id=data.response.question_id,
                answer_id=data.response.user_answer_id,
                selected_response=data.response.answer_text
            )

            db.add(user_response_instance)

        else:
            user_response_instance.answer_id = data.response.user_answer_id
            user_response_instance.selected_response = data.response.answer_text

        db.commit()
        db.refresh(user_response_instance)

        return {
            "message": "Session details saved successfully",
            "status_code": status.HTTP_200_OK
        }

    else:
        user_responses = (
            db.query(UserResponse)
            .join(Answer, UserResponse.answer_id == Answer.id)
            .filter(UserResponse.user_assessment_id == user_assessment_instance.id)
            .all()
        )

        questions = (
            db.query(Question)
            .filter(Question.assessment_id == user_assessment_instance.assessment_id)
            .all()
        )

        score = sum(
            user_response.selected_response == user_response.answer.correct_option
            for user_response in user_responses
        ) / len(questions) * 100


        user_assessment_instance.score = score
        user_assessment_instance.status = "complete"
        user_assessment_instance.time_spent = data.time_spent
        user_assessment_instance.submission_date = time.now()

        db.commit()

        badge_id = assign_badge(user_assessment_instance.id, token)


        return {
            "message": "Submission and grading successful",
            "status_code": status.HTTP_200_OK,
            "score": score,
            "badge_id": badge_id,
            "assessment_id": user_assessment_instance.assessment_id,
        }
    

def send_email(user_id,db:Session):
    # get user email and name
    user=db.query(User).filter(User.id==user_id).first()
    email_payload={
        "recipient":user.email,
        "name":f'{user.first_name} {user.last_name}',
        "service":"Taking Assessment",
        "call_to_action_link":"https://example.com"
    }
    response=requests.post(settings.MESSAGING,data=json.dumps(email_payload))
    # if response.status_code != 200:
    #     raise HTTPException(status_code=response.status_code,detail={"message":"Email Delivery Error"})
    # return response.status_code

def assign_badge( assessment_id, token):

    req = requests.post(
        f"{settings.BADGE_SERVICE}",
        headers={"Authorization": f"Bearer {token}"},
        data=json.dumps({"assessment_id": int(assessment_id)})
    )

    if req.status_code != 201:
        raise HTTPException(status_code=req.status_code, detail="Error assigning badge")
    return req.json()['data']['badge']['id']
    
    