from sqlalchemy.orm import Session
from app.models import UserAssessment, Question, UserResponse, Answer, Assessment,User
from app.schemas import UserAssessmentanswer
from fastapi import HTTPException, status
from app.response_schemas import Response
import requests
import json
from app.config import settings
from fastapi import BackgroundTasks


# save session details
def save_session(data: UserAssessmentanswer, user_id: int, db:Session, background_task: BackgroundTasks):

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
    user_assessment_instance = db.query(UserAssessment).filter(UserAssessment.user_id==user_id,UserAssessment.assessment_id==data.assessment_id, UserAssessment.status == "pending").first()

    if not user_assessment_instance:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="There is no match for user_id or assessment_id")

    if not data.is_submitted and  data.time_spent == None:
        User_Response = db.query(UserResponse).filter(UserResponse.user_assessment_id==user_assessment_instance.id,UserResponse.question_id==data.response.question_id).first()
        
        if not User_Response:
            
            userdata = UserResponse(
                user_assessment_id=user_assessment_instance.id,
                question_id=data.response.question_id,
                answer_id=data.response.user_answer_id,
                selected_response=data.response.answer_text
            )

            db.add(userdata)
            db.commit()
            db.refresh(userdata)

            return Response(message="Session details saved successfully",status_code=status.HTTP_200_OK)

        else:
            User_Response.answer_id = data.response.user_answer_id
            User_Response.selected_response = data.response.answer_text
            db.commit()
            db.refresh(User_Response)

            return Response(message="Session details saved successfully",status_code=status.HTTP_200_OK)

    else:

        try:

            # fetch all userresponse tied to the userassessment id
            userdata = db.query(UserResponse).filter(UserResponse.user_assessment_id==user_assessment_instance.id).all()

            # fetch all questions tied to the userassessment id
            questions = db.query(Question).filter(Question.assessment_id==user_assessment_instance.assessment_id).all()

            # calculate score
            score = 0

            for i in userdata:

                # fetch the answer tied to the question id
                answer = db.query(Answer).filter(Answer.question_id==i.question_id).first()

                # check if the user selected answer is equal to the correct answer
                if i.selected_response == answer.correct_option:
                    score += 1

            score = (score/len(questions))*100

            assessment_instance = db.query(Assessment).filter(Assessment.id==user_assessment_instance.assessment_id).first()
            # badges = db.query(SkillBadge).filter(SkillBadge.skill_id==assessment_instance.skill_id).all()

            # update the userassessment table with the score and status
            user_assessment_instance.score = score
            user_assessment_instance.status = "complete"
            user_assessment_instance.time_spent = data.time_spent
            db.commit()
            db.refresh(user_assessment_instance)

            # assign badge
            # badge = assign_badge(user_id, user_assessment_instance.id)
            # print(badge)
            # background_task.add_task(send_email, user_id, db)
            '''
            # check if each badge where the score falls within the range
            for badge in badges:

                if badge.min_score <= score <= badge.max_score:

                    user_assessment_instance.badge_id = badge.id
                    break
                continue

            badge = UserBadge(
                user_id=user_id,
                badge_id=user_assessment_instance.badge_id,
                assessment_id=user_assessment_instance.assessment_id
            )

            db.add(badge)
            db.commit()
            db.refresh(badge)
            '''
            return {
                "message":"Session details saved successfully",
                "status_code":status.HTTP_200_OK,
                "score":score,
                # "badge_id":badge,
                "assessment_id":user_assessment_instance.assessment_id,
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
    response=requests.post(settings.MESSAGING,data=json.dumps(email_payload))
    # if response.status_code != 200:
    #     raise HTTPException(status_code=response.status_code,detail={"message":"Email Delivery Error"})
    # return response.status_code

def assign_badge(user_id, assessment_id):

    req = requests.post(
        f"{settings.BADGE_SERVICE}",
        headers={},
        data={"user_id": user_id, "assessment_id":assessment_id})

    if req.status_code == 200:
        print(req.json())
        return req.json().get("data").get("badge").get("id")
    
    if req.status_code == 400:
        return req.text