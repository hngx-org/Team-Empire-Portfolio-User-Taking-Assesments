from pydantic import BaseModel
from typing import List
from app.schemas import STATUS

class StartAssessmentResponse(BaseModel):
    message: str
    status_code: int
    questions: list

class UserAssessmentResponse(BaseModel):
    id: int
    user_id: str
    assessment_id: int
    score: float
    status: STATUS
    submission_date: str