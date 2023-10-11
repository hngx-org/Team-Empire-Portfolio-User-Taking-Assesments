from pydantic import BaseModel
from typing import List
from app.schemas import STATUS, AssessmentAnswers


class AuthenticateUser(BaseModel):
    user_id: str
    is_super_admin: bool
    permissions: list


class Question(BaseModel):
    id: int
    question_text: str
    question_type: str


class Assessment(BaseModel):
    id: int
    title: str
    description: str
    questions: List[Question]


class UserAssessment(BaseModel):
    id: int
    user_id: str
    assessment_id: int
    score: float
    status: STATUS
    submission_date: str
    assessment: Assessment


class UserAssessmentResponse(BaseModel):
    message: str
    status_code: int
    assessments: List[UserAssessment]


class StartAssessmentResponse(BaseModel):
    message: str
    status_code: int
    questions: list


class AssessmentResults(BaseModel):
    score: float
    status: STATUS
    answers: list[AssessmentAnswers]
