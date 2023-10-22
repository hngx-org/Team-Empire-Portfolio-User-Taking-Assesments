from typing import List, Optional, Set

from pydantic import BaseModel

from app.schemas import STATUS, AssessmentAnswers


class Response(BaseModel):
    message: str
    status_code: int


class AuthenticateUser(BaseModel):
    id: str
    permissions: list


class Question(BaseModel):
    id: int
    question_text: str
    question_type: str


class Questions(BaseModel):
    question_id: int
    question_no: int
    question_text: str
    question_type: str
    answer_id: int
    user_selected_answer: Optional[str] = None
    options: Set


class StartAssessmentResponse(Questions):
    message: str
    status_code: int
    data: List[Questions]


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


class SingleAssessmentResponse(BaseModel):
    assessment_id: int
    skill_id: int
    title: str
    description: str
    duration_minutes: int
    pass_score: float
    status: STATUS
    start_date: str
    end_date: str


class AssessmentResults(BaseModel):
    score: float
    status: STATUS
    user_id: str
    assessment_id: int
    answers: list[AssessmentAnswers]
