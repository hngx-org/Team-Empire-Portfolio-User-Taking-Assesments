from pydantic import BaseModel
from typing import List, Set
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
    user_selected_answer: str | None= None
    options: Set
class StartAssessmentResponse(Questions):
    message: str
    status_code: int
    data:List[Questions]


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
    description : str
    duration_minutes : int
    pass_score: float
    status: STATUS
    start_date : str
    end_date: str

class AssessmentResults(BaseModel):
    score : float
    status : STATUS
    user_id : str
    assessment_id: int
    answers : list[AssessmentAnswers]
