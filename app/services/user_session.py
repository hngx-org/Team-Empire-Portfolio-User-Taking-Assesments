from sqlalchemy.orm import Session
from app.models import UserAssessment, Question, UserResponse, Answer, Assessment, SkillBadge,UserBadge,User
from app.schemas import UserAssessmentanswer
from fastapi import HTTPException, status
from app.response_schemas import Response
import requests
import json
from app.config import settings



# save session details
def save_session(data: UserAssessmentanswer, user_id: int, db:Session):

    """
    Save session details:
        This function saves the session details of a user

    Parameters:
    - data : SessionData
        SessionData object
    - user_id : int
        user id of the user

    Returns:
    - status_code : int
        status code of the response

    """
    user_assessment_instance = db.query(UserAssessment).filter(UserAssessment.user_id==user_id,UserAssessment.assessment_id==data.assessment_id).first()

    if not user_assessment_instance:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="There is no match for user_id or assessment_id")

    if not data.is_submitted:
        UserResponse = db.query(UserResponse).filter(UserResponse.user_assessment_id==user_assessment_instance.id,UserResponse.question_id==data.response.question_id).first()
        if UserResponse:
            UserResponse.answer_id = data.response.user_answer_id
            UserResponse.selected_response = data.response.answer_text
            db.commit()
            db.refresh(UserResponse)
            return Response(message="Session details saved successfully",status_code=status.HTTP_200_OK)

        else:

            try:

                data = UserResponse(
                    user_assessment_id=user_assessment_instance.id,
                    question_id=data.response.question_id,
                    answer_id=data.response.user_answer_id,
                    selected_response=data.response.answer_text
                )

                db.add(data)
                db.commit()
                db.refresh(data)

                return Response(message="Session details saved successfully",status_code=status.HTTP_200_OK)

            except Exception as e:
                print(e)
                return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="failed to save session details")

    else:

        try:

            # fetch all userresponse tied to the userassessment id
            data = db.query(UserResponse).filter(UserResponse.user_assessment_id==user_assessment_instance.id).all()

            # fetch all questions tied to the userassessment id
            questions = db.query(Question).filter(Question.assessment_id==user_assessment_instance.assessment_id).all()

            # calculate score
            score = 0

            for i in data:

                # fetch the answer tied to the question id
                answer = db.query(Answer).filter(Answer.question_id==i.question_id).first()

                # check if the user selected answer is equal to the correct answer
                if i.selected_response == answer.correct_option:
                    score += 1

            score = (score/len(questions))*100

            assessment_instance = db.query(Assessment).filter(Assessment.id==user_assessment_instance.assessment_id).first()
            badges = db.query(SkillBadge).filter(SkillBadge.skill_id==assessment_instance.skill_id).all()

            # update the userassessment table with the score and status
            user_assessment_instance.score = score

            # check if each badge where the score falls within the range
            for badge in badges:

                if badge.min_score <= score <= badge.max_score:

                    user_assessment_instance.badge_id = badge.id
                    break
                continue

            user_assessment_instance.status = "complete"

            db.commit()
            db.refresh(user_assessment_instance)

            badge = UserBadge(
                user_id=user_id,
                badge_id=user_assessment_instance.badge_id,
                assessment_id=user_assessment_instance.assessment_id
            )

            db.add(badge)
            db.commit()
            db.refresh(badge)

            return {
                "message":"Session details saved successfully",
                "status_code":status.HTTP_200_OK,
                "score":score,
                "badge":badge.badge_id
            }

        except Exception as e:
            print(e)
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="failed to calculate score")

def send_email(user_id,db:Session):
    # get user email and name
    user=db.query(User).filter(User.id==user_id).first()
    email_payload={
        "recipient":user.email,
        "name":f'{user.first_name} {user.last_name}',
        "service":"Taking Assessment",
        "call_to_action_link":"https://example.com"
    }
    response=requests.post(settings.MESSAGING_ENDPOINT,data=json.dumps(email_payload))
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,detail={"message":"Email Delivery Error"})
    return response.status_code
