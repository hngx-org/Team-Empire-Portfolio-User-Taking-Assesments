from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ForeignKey, Float, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.types import ARRAY

# Define ENUMs
STATUS = ENUM('pending', 'complete', 'failed', name='status_enum')
BADGES = ENUM('beginner', 'intermediate', 'expert', name='badges_enum')


class DATEBaseModel(Base):
    """
    DATEBaseModel Table

    It is an abstract model for tables that have created_at and updated_at columns.
    """
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, onupdate=text("now()"))


class BaseModel(Base):
    """
    BaseModel Table

    It is an abstract model for tables that have created_at, updated_at and id columns.
    """
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)


class UUIDBaseModel(Base):
    """
    UUIDBaseModel Table

    It is an abstract model for tables that have created_at, updated_at and id columns.
    """
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4)


class User(UUIDBaseModel):
    """
    User Table

    It is a model for user table in database.

    Columns:

    - username: username of the user.
    - first_name: first name of the user.
    - last_name: last name of the user.
    - email: email of the user.
    - password: password of the user.
    - section_order: order of the sections.
    - provider: provider of the user.
    - profile_pic: profile picture of the user.
    - refresh_token: refresh token of the user.

    Inherited columns:
    - id: primary key of the table.
    - created_at: created date of the record.
    - updated_at: updated date of the record.

    Relationships:

    - UserAssessment: one-to-many
    - UserBadge: one-to-many

    """

    __tablename__ = "user"
    username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    token = Column(String, nullable=True)
    password = Column(String, nullable=False)
    section_order = Column(Text, nullable=True)  # Explain section_order
    provider = Column(String, nullable=True)  # Explain provider
    profile_pic = Column(Text, nullable=True)
    refresh_token = Column(String, nullable=True)
    createdAt = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=text("now()"))
    updatedAt = Column(TIMESTAMP(timezone=True),
                       nullable=False, onupdate=text("now()"))

    user_assessment = relationship("UserAssessment", back_populates="user")
    user_badge = relationship("UserBadge", back_populates="user")


class UserAssessment(BaseModel):
    """
    UserAssessment Table

    It is a model for user_assessment table in database.

    Columns:
    - user_id: foreign key to user table.
    - assessment_id: foreign key to assessment table.
    - score: score of the assessment.
    - status: status of the assessment.
    - submission_date: submission date of the assessment.

    Inherited columns:
    - id: primary key of the table.
    - created_at: created date of the record.
    - updated_at: updated date of the record.

    Relationships:

    - User: one-to-many
    - Assessment: one-to-many
    - UserAssessmentProgress: one-to-many
    - UserResponse: one-to-many

    """
    __tablename__ = "user_assessment"  # this needs to be corrected
    user_id = Column(UUID, ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    assessment_id = Column(Integer, ForeignKey(
        "assessment.id", ondelete="CASCADE"), nullable=False)
    score = Column(Float)
    status = Column(STATUS, nullable=False, default="pending")
    time_spent = Column(Integer)
    submission_date = Column(TIMESTAMP(timezone=True),
                             nullable=False, server_default=text("now()"))

    user = relationship("User", back_populates="user_assessment")
    assessment = relationship("Assessment", back_populates="user_assessment")
    user_response = relationship(
        "UserResponse", back_populates="user_assessment")


class Assessment(BaseModel):
    """
    Assessment Table

    It is a model for assessment table in database.

    Columns:

    - skill_id: foreign key to skill table.
    - title: title of the assessment.
    - description: description of the assessment.
    - duration_minutes: duration of the assessment in minutes.
    - pass_score: minimum score to pass the assessment.
    - status: status of the assessment.
    - start_date: start date of the assessment.
    - end_date: end date of the assessment.

    Inherited columns:
    - id: primary key of the table.
    - created_at: created date of the record.
    - updated_at: updated date of the record.

    Relationships:

    - UserAssessment: one-to-many
    - Skill: one-to-many
    - AssessmentCategory: one-to-many
    - UserBadge: one-to-many

    """
    __tablename__ = "assessment"

    skill_id = Column(Integer, ForeignKey(
        "skill.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    duration_minutes = Column(Integer, nullable=False)
    pass_score = Column(Float, nullable=False)
    status = Column(STATUS, nullable=False, default="pending")
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)

    user_assessment = relationship(
        "UserAssessment", back_populates="assessment")
    skill = relationship("Skill", back_populates="assessment")
    assessment_category = relationship(
        "AssessmentCategory", back_populates="assessment")
    user_badge = relationship("UserBadge", back_populates="assessment")


class Skill(BaseModel):
    """
    Skill Table

    It is a model for skill table in database.

    Columns:

    - category_name: name of the skill.
    - description: description of the skill.
    - parent_skill_id: foreign key to skill table.

    Inherited columns:
    - id: primary key of the table.
    - created_at: created date of the record.
    - updated_at: updated date of the record.

    Relationships:

    - Assessment: one-to-many
    - Skill: one-to-many
    - Skill: one-to-many
    - SkillBadge: one-to-many
    - AssessmentCategory: one-to-many

    """
    __tablename__ = "skill"

    category_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    parent_skill_id = Column(Integer, ForeignKey(
        "skill.id", ondelete="CASCADE"), nullable=True)

    assessment = relationship("Assessment", back_populates="skill")
    parent_skill = relationship(
        "Skill", remote_side=[id], back_populates="child_skill")
    child_skill = relationship(
        "Skill", remote_side=[parent_skill_id], back_populates="parent_skill"
    )
    skill_badge = relationship("SkillBadge", back_populates="skill")
    assessment_category = relationship(
        "AssessmentCategory", back_populates="skill")


class Question(BaseModel):
    """
    Question Table

    It is a model for question table in database.

    Columns:

    - assessment_id: foreign key to assessment table.
    - question_text: text of the question.
    - question_type: type of the question.

    Inherited columns:
    - id: primary key of the table.
    - created_at: created date of the record.
    - updated_at: updated date of the record.

    Relationships:

    - Assessment: one-to-many
    - Answer: one-to-many
    - UserAssessmentProgress: one-to-many
    - UserResponse: one-to-many

    """
    __tablename__ = "question"

    assessment_id = Column(Integer, ForeignKey(
        "assessment.id", ondelete="CASCADE"), nullable=False)
    question_no = Column(Integer, nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String, nullable=False)

    assessment = relationship("Assessment", back_populates="question")
    answer = relationship("Answer", back_populates="question")
    user_response = relationship("UserResponse", back_populates="question")


class Answer(BaseModel):
    """
    Answer Table

    It is a model for answer table in database.

    Columns:

    - question_id: foreign key to question table.
    - answer_text: text of the answer.
    - is_correct: boolean value to indicate if the answer is correct or not.

    Inherited columns:
    - id: primary key of the table.
    - created_at: created date of the record.
    - updated_at: updated date of the record.

    Relationships:

    - Question: one-to-many
    - UserResponse: one-to-many
    """
    __tablename__ = "answer"

    question_id = Column(Integer, ForeignKey(
        "question.id", ondelete="CASCADE"), nullable=False)
    options = Column(ARRAY(String))
    correct_option = Column(String)

    question = relationship("Question", back_populates="answer")
    user_response = relationship("UserResponse", back_populates="answer")


class SkillBadge(DATEBaseModel):
    """
    SkillBadge Table

    It is a model for skill_badge table in database.

    Columns:

    - skill_id: foreign key to skill table.
    - name: name of the badge.
    - badge_image: image of the badge.
    - min_score: minimum score to get the badge.
    - max_score: maximum score to get the badge.

    Inherited columns:
    - id: primary key of the table.
    - created_at: created date of the record.
    - updated_at: updated date of the record.

    Relationships:

    - Skill: one-to-many
    - UserBadge: one-to-many

    """
    __tablename__ = "skill_badge"

    skill_id = Column(Integer, ForeignKey(
        "skill.id", ondelete="CASCADE"), nullable=False)
    name = Column(BADGES, nullable=False)
    badge_image = Column(Text, nullable=False)
    min_score = Column(Float, nullable=False)
    max_score = Column(Float, nullable=False)
    createdAt = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updatedAt = Column(
        TIMESTAMP(timezone=True), nullable=False, onupdate=text("now()")
    )

    skill = relationship("Skill", back_populates="skill_badge")
    user_badge = relationship("UserBadge", back_populates="badge")


class UserResponse(BaseModel):
    """
    UserResponse Table

    It is a model for user_response table in database.

    Columns:

    - user_assessment_id: foreign key to user_assessment table.
    - question_id: foreign key to question table.
    - answer_id: foreign key to answer table.

    Inherited columns:
    - id: primary key of the table.
    - created_at: created date of the record.
    - updated_at: updated date of the record.

    Relationships:

    - UserAssessment: one-to-many
    - Question: one-to-many
    - Answer: one-to-many

    """
    __tablename__ = "user_response"

    user_assessment_id = Column(Integer, ForeignKey(
        "user_assessment.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey(
        "question.id", ondelete="CASCADE"), nullable=False)
    answer_id = Column(Integer, ForeignKey(
        "answer.id", ondelete="CASCADE"), nullable=False)
    selected_response = Column(Text)

    user_assessment = relationship(
        "UserAssessment", back_populates="user_response")
    question = relationship("Question", back_populates="user_response")
    answer = relationship("Answer", back_populates="user_response")


class AssessmentCategory(BaseModel):
    """
    AssessmentCategory Table

    It is a model for assessment_category table in database.

    Columns:

    - assessment_id: foreign key to assessment table.
    - skill_id: foreign key to skill table.

    Inherited columns:
    - id: primary key of the table.
    - created_at: created date of the record.
    - updated_at: updated date of the record.

    Relationships:

    - Assessment: one-to-many
    - Skill: one-to-many

    """
    __tablename__ = "assessment_category"

    assessment_id = Column(Integer, ForeignKey(
        "assessment.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey(
        "skill.id", ondelete="CASCADE"), nullable=False)

    assessment = relationship(
        "Assessment", back_populates="assessment_category")
    skill = relationship("Skill", back_populates="assessment_category")


class UserBadge(DATEBaseModel):
    """
    UserBadge Table

    It is a model for user_badge table in database.

    Columns:

    - user_id: foreign key to user table.
    - badge_id: foreign key to skill_badge table.
    - assessment_id: foreign key to assessment table.

    Inherited columns:
    - id: primary key of the table.
    - created_at: created date of the record.
    - updated_at: updated date of the record.

    It has the following relationships:

    - User: one-to-many
    - SkillBadge: one-to-many
    - Assessment: one-to-many
    """
    __tablename__ = "user_badge"

    user_id = Column(UUID, ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    badge_id = Column(Integer, ForeignKey(
        "skill_badge.id", ondelete="CASCADE"), nullable=False)
    assessment_id = Column(Integer, ForeignKey(
        "assessment.id", ondelete="CASCADE"), nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=text("now()"))
    updatedAt = Column(TIMESTAMP(timezone=True),
                       nullable=False, onupdate=text("now()"))

    user = relationship("User", back_populates="user_badge")
    badge = relationship("SkillBadge", back_populates="user_badge")
    assessment = relationship("Assessment", back_populates="user_badge")

# Path: app/router.py
