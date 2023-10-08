from pydantic import BaseModel
from typing import Text, List, Optional
from uuid import UUID
from enum import Enum


# Query fields
class StartAssessment(BaseModel):
    user_id: str
    assessment_id:int