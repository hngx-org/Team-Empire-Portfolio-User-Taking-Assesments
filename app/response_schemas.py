from pydantic import BaseModel
from typing import List
from app.schemas import STATUS, AssessmentAnswers

class Response(BaseModel):
    message: str
    status_code: int
class AuthenticateUser(BaseModel):
    id: str
    is_super_admin: bool
    permissions: list


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

class AssessmentResults(BaseModel):
    score : float
    status : STATUS
    answers : list[AssessmentAnswers]