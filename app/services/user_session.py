from sqlalchemy.orm import Session
from app.models import UserAssessment, Question, UserResponse, Answer
from app.schemas import UserAssessmentanswer
from fastapi import HTTPException, status
from app.response_schemas import Response


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
    user_assessment_id = db.query(UserAssessment).filter(UserAssessment.user_id==user_id,UserAssessment.assessment_id==data.assessment_id).first()
    if not data.is_submitted:

        if not user_assessment_id:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="There is no match for user_id or assessment_id")
        
        try:
            data = UserResponse(
                user_assessment_id=user_assessment_id.id,
                question_id=data.response.question_id,
                answer_id=data.response.user_answer_id,
                selected_text=data.response.answer_text
            )
            db.add(data)
            db.commit()
            db.refresh(data)
            return Response(message="Session details saved successfully",status_code=status.HTTP_200_OK)
        except:
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="failed to save session details")
    else: 
  
        try:
            # fetch all userresponse tied to the userassessment id

            data = db.query(UserResponse).filter(UserResponse.user_assessment_id==user_assessment_id.id).all()

            # fetch all questions tied to the userassessment id
            questions = db.query(Question).filter(Question.assessment_id==user_assessment_id.assessment_id).all()
            # fetch all answers tied to the userassessment id
            answers = db.query(Answer).filter(Answer.question_id==Question.id).all()
            # calculate score
            score = 0
            for question in questions:
                for answer in answers:
                    if answer.is_correct:
                        score += 1
            score = (score/len(questions))*100
            # update the userassessment table with the score and status
            user_assessment_id.score = score
            # check if the score is greater thanassessment passing score
            if score >= user_assessment_id.assessment.passing_score:
                user_assessment_id.status = "complete"
            else:
                user_assessment_id.status = "failed"

            db.commit()
            db.refresh(user_assessment_id)

            # TODO: send score to badges service
            return Response(message="Session details saved successfully",status_code=status.HTTP_200_OK)
        except:
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="failed to calculate score")
