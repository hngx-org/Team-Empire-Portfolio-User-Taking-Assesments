from datetime import datetime
from fastapi import HTTPException, status
from typing import List, Optional
from pydantic import BaseModel

# Simulate 'database' with list
session_progress_db = []
user_session_db = []

# Pydantic models. Will move to right folders once task is validated
class Response(BaseModel):
    question_id: int
    answer_id: Optional[int] = None

class SessionData(BaseModel):
    assessment_id: int
    time_remaining: int
    responses: List[Response]
    
class Assessment(BaseModel):

    skill_id : int
    title : str
    description : Optional[str]
    duration_minutes : int
    pass_score : float
    status : str
    start_date : datetime
    end_date : datetime
    
class AssessmentSession(Assessment):
    id : int
    time_remaining : int
    
class Question(BaseModel):
    assessment_id : int
    question_text : str
    question_type : str

class QuestionOut(Question):
    id: int
    
class Answer(BaseModel):
    answer_txt: str

class AnswerOut(Answer):
    id: int
    
class SessionQuestionAnswer(QuestionOut):
    answers: Optional[List[AnswerOut]] = None
    answer_id: int

class AssessmentSessionData(AssessmentSession):
    id: int
    questions: Optional[List[SessionQuestionAnswer]] = None

    class Config:
        from_attributes = True

# save session details
def save_session(data: SessionData, user_id: int):

    """
    Save session details:
        This function saves the session details of a user

    Parameters:
    - data : SessionData
        SessionData object
    - user_id : int
        user id of the user

    Returns:
    - status_code : int
        status code of the response

    """
    global session_progress_db, user_session_db

    # check if there is previous draft in the db
    existing_progress = next((item for item in session_progress_db if item['assessment_id'] == data.assessment_id and item['user_id'] == user_id), None)

    # if yes, update time for progress and remove user_session instances
    if existing_progress:
        session_progress_db.remove(existing_progress)
        user_session_db = [item for item in user_session_db if not (item['assessment_id'] == data.assessment_id and item['user_id'] == user_id)]

    user_responses = [{"question_id": response.question_id, "answer_id": response.answer_id, "user_id": user_id, "assessment_id": data.assessment_id} for response in data.responses]

    session_progress = {"user_id": user_id, "assessment_id": data.assessment_id, "time_remaining": data.time_remaining}
    
    # save new session details to database
    session_progress_db.append(session_progress)
    user_session_db.extend(user_responses)
    
    return {"status_code": status.HTTP_201_CREATED}

# get all sessions
def get_all_session(user_id: int):
    """
    Get all sessions:
        This function gets all the sessions of a user

    Parameters:
    - user_id : int
        user id of the user

    Returns:
    - sessions : List[AssessmentSession]
        list of AssessmentSession objects

    """
    return [item for item in session_progress_db if item['user_id'] == user_id]

# Dummy assessment data
assessments_db = [{
    "id": 1,
    "skill_id": 101,
    "title": "Sample Assessment",
    "description": "This is a sample assessment.",
    "duration_minutes": 30,
    "pass_score": 0.5,
    "status": "active",
    "start_date": "2023-10-06T00:00:00",
    "end_date": "2023-10-30T00:00:00",
    "questions": [{
        "id": 1,
        "assessment_id": 1,
        "question_text": "Sample question",
        "question_type": "MCQ",
        "answers": [{"id": 1, "answer_txt": "Sample answer"}]
    }]
}]

# get a session details
def get_session_detail(user_id: int, assessment_id: int):
    """
    Get session details:
        This function gets the session details of a user

    Parameters:
    - user_id : int
        user id of the user
    - assessment_id : int
        assessment id of the assessment

    Returns:
    - assessment_dict : AssessmentSessionData
        AssessmentSessionData object

    """
    
    # validate that such call is possible
    session_progress = next((item for item in session_progress_db if item['assessment_id'] == assessment_id and item['user_id'] == user_id), None)
    
    if not session_progress:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no session found for details given")
    
    # ftch session details ie questions and answers previously saved
    sessions = [item for item in user_session_db if item['assessment_id'] == assessment_id and item['user_id'] == user_id]

    # Fetching assessment from dummy list
    assessment = next((a for a in assessments_db if a["id"] == assessment_id), None)

    # convert query to jsonable_encoder and update fields
    # ie get all questions and options along with user already answered questions
    assessment_dict = assessment.copy()
    assessment_dict['time_remaining'] = session_progress['time_remaining']

    for i, question in enumerate(assessment_dict['questions']):
        answer_id = None
        for ses in sessions:
            if ses['question_id'] == question['id']:
                answer_id = ses['answer_id']
        assessment_dict['questions'][i]['answer_id'] = answer_id

    return assessment_dict

