from pydantic import BaseModel
from typing import Text, List, Optional, Union
from uuid import UUID
from enum import Enum

class AssessmentAnswers(BaseModel):
    question_text : str 
    answer_text: str
    
class STATUS(Enum):
    pending = "pending"
    complete = "complete"
    failed = "failed"

class BADGES(Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    expert = "expert"

# User schema
class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    password: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: UUID
    provider: Optional[str] = None
    section_order: Optional[Text] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    profile_pic: Optional[Text] = None
    refresh_token: Optional[str] = None
    user_assessment: List["UserAssessment"] = []
    user_badge: List["UserBadge"] = []

    class Config:
        from_attributes = True

# UserAssessment schema
class UserAssessmentBase(BaseModel):
    score: float
    status: STATUS

class UserAssessmentCreate(UserAssessmentBase):
    pass


class UserAssessment(UserAssessmentBase):
    id: int
    user_id: UUID
    assessment_id: int
    submission_date: Optional[str] = None
    user_response: List["UserResponse"] = []
    user_assessment_progress: List["UserAssessmentProgress"] = []
    user: Optional[User] = None
    assessment: Optional["Assessment"] = None

    class Config:
        from_attributes = True

# User Badge
class UserBadgeBase(BaseModel):
    user_id: UUID
    badge_id: UUID
    assessment_id: UUID


class UserBadgeCreate(UserBadgeBase):
    pass


class UserBadge(UserBadgeBase):
    id: UUID
    user: Optional[User] = None
    badge: Optional["SkillBadge"] = None

    class Config:
        from_attributes = True

# Skill badge schema


class SkillBadgeBase(BaseModel):
    skill_id: int
    name: BADGES
    badge_image: Text
    min_score: float
    max_score: float


class SkillBadgeCreate(SkillBadgeBase):
    pass


class SkillBadge(SkillBadgeBase):
    id: UUID
    skill: Optional["Skill"] = None
    user_badge: List[UserBadge] = []

    class Config:
        from_attributes = True

# Assessment schema


class AssessmentBase(BaseModel):
    title: str
    description: Text
    pass_score: float


class AssessmentCreate(AssessmentBase):
    duration_minutes: int
    skill_id: int


class Assessment(AssessmentBase):
    id: int
    status: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    user_assessment: List["UserAssessment"] = []
    skill: Optional["Skill"] = None

    class Config:
        from_attributes = True

# Skill schema


class SkillBase(BaseModel):
    category_name: str
    description: Text


class SkillCreate(SkillBase):
    pass


class Skill(SkillBase):
    id: int
    parent_skill_id: Optional[int] = None
    child_skill: List["Skill"] = []
    assessment: List[Assessment] = []

    class Config:
        from_attributes = True

# UserResponse schema


class UserResponseBase(BaseModel):
    question_id: int
    answer_id: int


class UserResponseCreate(UserResponseBase):
    pass


class UserResponse(UserResponseBase):
    id: int
    user_assessment_id: int
    user_assessment_progress: List["UserAssessmentProgress"] = []

    class Config:
        from_attributes = True

# UserAssessmentProgress schema


class UserAssessmentProgressBase(BaseModel):
    user_assessment_id: int
    question_id: int
    status: str


class UserAssessmentProgressCreate(UserAssessmentProgressBase):
    pass


class UserAssessmentProgress(UserAssessmentProgressBase):
    id: int

    class Config:
        from_attributes = True

# Question schema


class QuestionBase(BaseModel):
    assessment_id: int
    question_text: Text
    question_type: str


class QuestionCreate(QuestionBase):
    pass


class Question(QuestionBase):
    id: int
    assessment: Optional[Assessment] = None
    answer: List["Answer"] = []
    user_assessment_progress: List[UserAssessmentProgress] = []
    user_response: List[UserResponse] = []

    class Config:
        from_attributes = True

# Answer schema


class AnswerBase(BaseModel):
    question_id: int
    answer_text: Text
    is_correct: bool


class AnswerCreate(AnswerBase):
    pass


class Answer(AnswerBase):
    id: int
    question: Optional[Question] = None
    user_response: List[UserResponse] = []

    class Config:
        from_attributes = True


# Query fields
class StartAssessment(BaseModel):
    #user_id: str #the user id will henceforth be extracted from header token
    assessment_id:int

class UserAssessmentQuery(BaseModel):
    user_id: str


class userResponse(BaseModel):
    question_id: int = None
    user_answer_id: int = None
    answer_text:str = None

class UserAssessmentanswer(BaseModel):
    assessment_id: int
    is_submitted: bool = False 
    time_spent: int = None
    response: Union[userResponse, None]= None
    


