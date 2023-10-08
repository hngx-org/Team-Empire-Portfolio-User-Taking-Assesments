from pydantic import BaseModel
from typing import Text, List, Optional
from uuid import UUID
from enum import Enum

class AssessmentAnswers(BaseModel):
    question_text : str
    answer_text: str