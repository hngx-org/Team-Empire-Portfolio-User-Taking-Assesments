from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from app.models import UserAssessment
from app.fake_db_response import UserAssessments as fake_db_user_assessments
from app.fake_db_response import User


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
    
    assessments = [assessment for assessment in fake_db_user_assessments if assessment.get('user_id') == user_id]
    return assessments

def get_user_by_id(user_id: str, db: Session):
    """
    Get user by user_id:
        This function retrieves a user based on their user_id.

    Parameters:
    - user_id : str
        User ID of the user.
    - db : Session
        Database session.

    Returns:
    - user : User
        User object if found, None if not found.
    """
    # Replace when live database
    #user = db.query(User).filter(User.id == user_id).first()
    return User