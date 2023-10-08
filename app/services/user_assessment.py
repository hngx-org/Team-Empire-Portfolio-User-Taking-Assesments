from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from app.models import UserAssessment
from app.fake_db_response import UserAssessments as fake_db_user_assessments

def get_user_assessments_from_db(user_id: str,db=Session):
    """
    Get user assessments:
        This function gets the assessments of a user

    Parameters:
    - user_id : str
        user id of the user
    - db : Session
        database session

    Returns:
    - assessments : List[UserAssessment]
        list of UserAssessment objects
        
    """
    # Replace when live data is available on DB
    # assessments = db.query(UserAssessment).filter(UserAssessment.user_id == user_id).all()

    assessments = [assessment for assessment in fake_db_user_assessments if assessment['user_id'] == user_id]
    return assessments