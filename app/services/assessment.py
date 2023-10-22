from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import UserAssessment





def get_completed_assessments(user_id,db:Session):
    completed_assessments=db.query(UserAssessment).filter(UserAssessment.user_id==user_id,UserAssessment.status=='complete').all()
    if completed_assessments==[]:
        return None,HTTPException(status_code=404,detail={
            "message":"No completed assessments found",
            "status_code":404,
            "data":{}
        })

    response = [
        {
            "id": assessment.id,
            "user_id": assessment.user_id,
            "assessment_id": assessment.assessment_id,
            "score": assessment.score,
            "status": assessment.status,
            "submission_date": assessment.submission_date,
            "skill_id": assessment.user_badge[0].skill_badge.skill_id
            if assessment.user_badge
            else None,
            "assessment_name": assessment.assessment.title
            if assessment.assessment
            else None,
            "badge_id": assessment.user_badge[0].id
            if assessment.user_badge
            else None,
            "badge_name": assessment.user_badge[0].skill_badge.name
            if assessment.user_badge
            else None,
        }
        for assessment in completed_assessments
    ]
    return response,None

