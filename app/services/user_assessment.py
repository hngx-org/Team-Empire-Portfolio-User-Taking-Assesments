from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from app.models import UserAssessment, Question, UserResponse, Answer, Assessment, Track, UserTrack, Skill


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
    user_track = db.query(UserTrack).filter(UserTrack.user_id==user_id).first()
    # print(user_track.track_id)
    if not user_track:
        return None, HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No track found for this user")
    
    track = db.query(Track).filter(Track.id==user_track.track_id).first()

    
    if not track:
        return None, HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No track found for this user")
    
    skill = db.query(Skill).filter(Skill.category_name==track.track).first()

    if not skill:
        return None, HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No skill found for this user")
    
    assessments = db.query(Assessment).filter(Assessment.skill_id==skill.id).all()

#######################################################################################################################
#     assessments = (
#     db.query(Assessment)
#     .join(Skill, Assessment.skill_id == Skill.id)
#     .join(Track, Skill.category_name == Track.track)
#     .join(UserTrack, UserTrack.track_id == Track.id)
#     .filter(UserTrack.user_id == user_id)
#     .all()
# )

    if not assessments:
        return None, HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No assessments found for this user")
    
    return assessments, None