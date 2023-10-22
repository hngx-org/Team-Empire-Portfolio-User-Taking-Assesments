from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Assessment, Question, Skill, Track, UserAssessment, UserTrack


def get_user_assessments_from_db(user_id: str, db: Session):
    """
    Get user assessments:
        This function gets the assessments of a user

    Parameters:
    - user_id : str
        user id of the user
    - db : Session
        database session

    Returns:
    - assessments : List[Assessment]
        list of Assessment objects a user can take

    """
    user_track = (
        db.query(UserTrack, Track, Skill)
        .join(Track, UserTrack.track_id == Track.id)
        .join(Skill, Track.track == Skill.category_name)
        .filter(UserTrack.user_id == user_id)
        .first()
    )

    if not user_track:
        return None, HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "No user track found",
                "status_code": status.HTTP_404_NOT_FOUND,
                "data": {},
            },
        )

    # Get all assessments for the user's skill category
    assessments = (
        db.query(Assessment)
        .join(Question, Assessment.id == Question.assessment_id, isouter=True)
        .filter(Assessment.skill_id == user_track.Skill.id)
        .group_by(Assessment.id)
        .having(func.count(Question.id) > 0)
        .all()
    )

    if not assessments:
        return None, HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "No assessments found",
                "status_code": status.HTTP_404_NOT_FOUND,
                "data": {},
            },
        )

    # Get user assessments
    user_assessments = (
        db.query(UserAssessment).filter(UserAssessment.user_id == user_id).all()
    )

    # Create a set of assessment ids that the user has taken
    taken_assessment_ids = {ua.assessment_id for ua in user_assessments}

    # Add a "taken" attribute to each assessment object
    for assessment in assessments:
        assessment.taken = assessment.id in taken_assessment_ids

    return assessments, None
