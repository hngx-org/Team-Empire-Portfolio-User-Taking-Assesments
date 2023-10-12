from pydantic import BaseModel
from typing import List, Set
from app.schemas import STATUS, AssessmentAnswers

class Response(BaseModel):
    message: str
    status_code: int
class AuthenticateUser(BaseModel):
    id: str
    is_super_admin: bool
    permissions: list

class Questions(BaseModel):
    question_id: int
    question_no: int
    question_text: str
    question_type: str
    user_selected_answer: str | None= None
    options: Set
class StartAssessmentResponse(Questions):
    message: str
    status_code: int
    data:List[Questions]


class UserAssessmentResponse(BaseModel):
    id: int
    user_id: str
    assessment_id: int
    score: float
    status: STATUS
    submission_date: str

class SingleAssessmentResponse(BaseModel):
    assessment_id: int
    skill_id: int
    title: str
    description : str
    duration_minutes : int
    pass_score: float
    status: STATUS
    start_date : str
    end_date: str

class AssessmentResults(BaseModel):
    score : float
    status : STATUS
    answers : list[AssessmentAnswers]