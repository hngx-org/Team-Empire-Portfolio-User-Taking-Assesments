from fastapi import APIRouter, HTTPException, status, Depends,Response
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.external import (
        check_for_assessment,
        fetch_questions,
        fetch_single_assessment, 
        fetch_answered_and_unanswered_questions
    )
from app.services.user_assessment import get_user_assessments_from_db
from app.services.assessment import get_assessment_results
from app.schemas import StartAssessment, UserAssessmentQuery
from app.response_schemas import StartAssessmentResponse, UserAssessmentResponse, AssessmentResults,SingleAssessmentResponse
from app.services.user_session import  save_session
from app.config import Permission, settings
from app.services.external import fake_authenticate_user, authenticate_user
from app.response_schemas import AuthenticateUser
from app.schemas import StartAssessment, UserAssessmentQuery,UserAssessmentanswer
from app.response_schemas import StartAssessmentResponse, UserAssessmentResponse, Questions

if settings.ENVIRONMENT == "development":
    authenticate_user = fake_authenticate_user

# Create a router object
router = APIRouter(tags=["Assessments"], prefix="/assessments")


@router.get("/{user_id}", response_model=List[UserAssessmentResponse])
async def get_all_user_assessments(user_id:str, db:Session = Depends(get_db), user:AuthenticateUser=Depends(authenticate_user)):
    """

    Retrieve all assessments taken by a user.

    Method: GET
    Request: User ID
    Response:

        - message: Message indicating the status of the request
        - status_code: Status code of the request
        - assessments: List of assessments taken by the user

    Error Response:

        - message: Message indicating the status of the request
        - status_code: Status code of the request

    Example request:
    
            curl -X GET "http://localhost:8000/api/assessments/?user_id=1" -H  "accept: application/json"

    Example response:


            {
            "message": "Assessments fetched successfully",
            "status_code": 200,
            assessments: [
                {
                    "id": 1,
                    "user_id": "1",
                    "assessment_id": 1,
                    "score": 0.0,
                    "status": "in_progress",
                    "submission_date": "2021-09-08T15:43:00.000Z",
                    "assessment": {
                        "id": 1,
                        "name": "Python Assessment",
                        "description": "This is a python assessment",
                        "questions": [
                            {
                                "id": 1,
                                "question_text": "What is Python?",
                                "question_type": "MCQ"
                            },
                            {
                                "id": 2,
                                "question_text": "What is Python used for?",
                                "question_type": "MCQ"
                            },
                            {
                                "id": 3,
                                "question_text": "What is the difference between a list and a tuple?",
                                "question_type": "MCQ"
                            },
                            {
                                "id": 4,
                                "question_text": "What is the difference between a list and a dictionary?",
                                "question_type": "MCQ"
                            },
                            {
                                "id": 5,
                                "question_text": "What is the difference between a list and a set?",
                                "question_type": "MCQ"
                            },
                            {
                                "id": 6,
                                "question_text": "What is the difference between a set and a dictionary?",
                                "question_type": "MCQ"
                            },
                            {
                                "id": 7,
                                "question_text": "What is the difference between a tuple and a dictionary?",
                                "question_type": "MCQ"
                            },
                            {
                                "id": 8,
                                "question_text": "What is the difference between a tuple and a set?",
                                "question_type": "MCQ"
                            },
                            {
                                "id": 9,
                                "question_text": "What is the difference between a dictionary and a set?",
                                "question_type": "MCQ"
                            },
                            {
                                "id": 10,
                                "question_text": "What is the difference between a list, a tuple, a dictionary and a set?",
                                "question_type": "MCQ"
                            }
                        ]
                    }
                }
            ]
        }

    Error response:
    
    
                {
                "message": "No assessments found for this user",
                "status_code": 404
                }

    Error response:

                {
                "message": "User does not exist",
                "status_code": 404
                }

    Error response:

                {
                "message": "User ID is required",
                "status_code": 400
                }

    Error response:

    {
    message: "failed to fetch assessments",
    status_code: 500
    }
    """
    if not Permission.check_permission(user.permissions, "assessments::view"):

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User does not have permission to view assessments")
    
    assessments = get_user_assessments_from_db(user_id=user_id, db=db)
   
    
    return assessments
  


@router.post("/start-assessment",)
async def start_assessment(request:StartAssessment,response:Response,db:Session = Depends(get_db), user:AuthenticateUser=Depends(authenticate_user)):
    '''
    Start an assessment for a user.

    Method: POST
    Request_body: User ID, Assessment ID

    Response:
    
            - message: Message indicating the status of the request
            - status_code: Status code of the request
            - questions: List of questions for the assessment

    Error Response:

            - message: Message indicating the status of the request
            - status_code: Status code of the request

    Example request:

            curl -X POST "http://localhost:8000/api/assessments/start-assessment" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"user_id\":\"1\",\"assessment_id\":1}"

    Example response:

            {
            "message": "Assessment started successfully",
            "status_code": 200,
            "questions": [
                {
                    "id": 1,
                    "question_number":1,
                    "question_text": "What is Python?",
                    "question_type": "MCQ",
                    "options":["A. option 1","B. another answer","C. third option"]
                },
                {
                    "id": 2,
                    "question_number":2,
                    "question_text": "What is Python used for?",
                    "question_type": "MCQ",
                    "options":["A. option A","B. another answer","C. third option"]
                },
                {
                    "id": 3,
                    "question_number":3,
                    "question_text": "What is the difference between a list and a tuple?",
                    "question_type": "MCQ",
                    "options":["A. option 1","B. another answer","C. third option"]
                },
                {
                    "id": 4,
                    "question_number":4,
                    "question_text": "What is the difference between a list and a dictionary?",
                    "question_type": "MCQ",
                    "options":["A. first option ","B.another answer","C. third option"]
                },
                {
                    "id": 5,
                    "question_number":5,
                    "question_text": "What is the difference between a list and a set?",
                    "question_type": "MCQ",
                    "options":["A. option A","B. another answer","C. third option"]
                },
                {
                    "id": 6,
                    "question_number":6,
                    "question_text": "What is the difference between a set and a dictionary?",
                    "question_type": "MCQ",
                    "options":["A. option A","B. another answer","C. third option"]
                },
                {
                    "id": 7,
                    "question_number":7,
                    "question_text": "What is the difference between a tuple and a dictionary?",
                    "question_type": "MCQ",
                    "options":["A. option A","B. another answer","C. third option"]
                },
                {
                    "id": 8,
                    "question_number":8,
                    "question_text": "What is the difference between a tuple and a set?",
                    "question_type": "MCQ"
                    "options":["A. option A","B. another answer","C. third option"]
                },
                {
                    "id": 9,
                    "question_number":9,
                    "question_text": "What is the difference between a dictionary and a set?",
                    "question_type": "MCQ",
                    "options":["A. option A","B. another answer","C. third option"]
                },
                {
                    "id": 10,
                    "question_number":10,
                    "question_text": "What is the difference between a list, a tuple, a dictionary and a set?",
                    "question_type": "MCQ",
                    "options":["A. option A","B. another answer","C. third option"]
                }
            ]
        }

    Error response:
    
                    {
                    "message": "Assessment already started",
                    "status_code": 400
                    }

    Error response:
    
                        {
                        "message": "Assessment does not exist",
                        "status_code": 404
                        }

    Error response:
        
                            {
                            "message": "User does not exist",
                            "status_code": 404
                            }

    Error response:
            
                                    {
                                    "message": "User ID is required",
                                    "status_code": 400
                                    }

    Error response:
        
        {
        message: "failed to start assessment",
        status_code: 500
        }

    '''
    if not Permission.check_permission(user.permissions, "assessment.update.own"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User does not have permission to start assessments")
    
    assessment_id = request.assessment_id
    user_assessment_instance,err = check_for_assessment(user_id=user.id,assessment_id=assessment_id,db=db)
    
    #check for corresponding matching id
    if err:
        raise err
    if not user_assessment_instance:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Critical error occured while getting assessment details")
    
    #retrieve assessment duration for setting cookies
    duration = user_assessment_instance.assessment["duration_minutes"]
    duration_seconds = duration*60
    response.set_cookie(key="assessment_duration",value= f"{duration_seconds}",expires=duration_seconds)
    response.set_cookie(key="assessment_session",value= f"{assessment_id}",expires=duration_seconds)

    #get all questions for the assessment
    questions_instance,error = fetch_questions(assessment_id=assessment_id,db=db)

    #check for availability of questions under the assessment_id
    if error:
        raise error
    if not questions_instance:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Critical error occured while fetching questions")
    
    #extract question(id,text type) and append to questions list
    question_list =[]
    for question in questions_instance:
        question_list.append(Questions(
            question_id=question.id,
            question_no=question.question_no,
            question_text=question.question_text,
            question_type=question.question_type, 
            options=question.answer.options
            ))

    response = {
        "message": "Assessment started successfully",
        "status_code": 200,
        "data": question_list
    }


@router.get("/session")
async def get_session_details(response:Response,db:Session = Depends(get_db), user:AuthenticateUser=Depends(authenticate_user)):

    #get assessment id from cookie
    assessment_id = response.cookies.get("assessment_session")
    #get duration from cookie
    duration = response.cookies.get("assessment_duration")
    
    #check for assessment id and duration
    if not assessment_id or not duration:
        redirect_url = f"{settings.FRONTEND_URL}/assessments" #get frontend url from env
        response.headers["Location"] = redirect_url
        response.status_code = status.HTTP_302_FOUND
        return response

    unanswered_question, answered_question, error = fetch_answered_and_unanswered_questions(assessment_id=assessment_id, user_id=user.id,db=db)
    if error:
        raise error
    if not unanswered_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Assessment already completed")

    answered_question_list = []
    unanswered_question_list = []
    
    for question in answered_question:
        answered_question_list.append(Questions(
            question_id=question.id,
            question_no=question.question.question_no,
            question_text=question.question.question_text,
            question_type=question.question.question_type, 
            options=question.answer.options,
            user_selected_answer= question.selected_response,
            ))
        
    for question in unanswered_question:
        unanswered_question_list.append(Questions(
            question_id=question.id,
            question_no=question.question_no,
            question_text=question.question_text,
            question_type=question.question_type,
            options=question.answer.options
            ))
        
    response = {
        "message": "Session details fetched successfully",
        "status_code": 200,
        "data": {
            "answered_questions": answered_question_list,
            "unanswered_questions": unanswered_question_list
        }
    }

@router.get("/{assessment_id}/result", status_code=200, response_model=AssessmentResults)
async def get_assessment_result(
    assessment_id: int,
    user_id: str,
    db: Session = Depends(get_db), 
    user:AuthenticateUser=Depends(authenticate_user)
):
    """
    Retrieve assessment results for a user.

    Method: GET
    Request: User ID, Assessment ID

    Response:

        - score: Score of the assessment
        - status: Status of the assessment
        - answers: List of answers submitted by the user

    Error Response:
    
            - message: Message indicating the status of the request
            - status_code: Status code of the request   

    Example request:

            curl -X GET "http://localhost:8000/api/assessments/1/result?user_id=1" -H  "accept: application/json"

    Example response:

            {
            "score": 0.0,
            "status": "in_progress",
            "answers": []
            }

    Error response:

                {
                "message": "Assessment does not exist",
                "status_code": 404
                }

    Error response:
    
                    {
                    "message": "User does not exist",
                    "status_code": 404  
                    }


    """
    if not Permission.check_permission(user.permissions, "assessment.read"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User does not have permission to view results")
    
    score, assessment_status, answers = get_assessment_results(user_id=user_id, assessment_id=assessment_id, db=db)
    
    response = {
        "score": score,
        "status": assessment_status,
        "answers": answers
    }
    

    return response

@router.post("/submit", )
async def submit_assessment(
    response:UserAssessmentanswer, db: Session = Depends(get_db), user: AuthenticateUser = Depends(authenticate_user)
):
    """
    Submit an assessment for a user.

    Method: POST
    Request_body: User ID, Assessment ID, Answers

    Response:
    
            - message: Message indicating the status of the request
            - status_code: Status code of the request

    Error Response:

            - message: Message indicating the status of the request
            - status_code: Status code of the request

    Example request:

            curl -X POST "http://localhost:8000/api/assessments/1/submit" -H  "accept: application/json" -H  \
            "Content-Type: application/json" -d "{\"user_id\":\"1\",\"assessment_id\":1,\"answers\":[{\"question_id\":1,\"user_answer_id\":1},\
                {\"question_id\":2,\"user_answer_id\":2},{\"question_id\":3,\"user_answer_id\":3},{\"question_id\":4,\"user_answer_id\":4},\
                    {\"question_id\":5,\"user_answer_id\":5},{\"question_id\":6,\"user_answer_id\":6},{\"question_id\":7,\"user_answer_id\":7},\
                        {\"question_id\":8,\"user_answer_id\":8},{\"question_id\":9,\"user_answer_id\":9},{\"question_id\":10,\"user_answer_id\":10}]}"

    Example response:
    
                {
                "message": "Assessment submitted successfully",
                "status_code": 200
                }

    """
    if not Permission.check_permission(user.permissions, "assessment.update.own"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User does not have permission to submit assessments")
    
    # check if user is eligible to submit assessment at first if required
    # user_id comes from auth
    return save_session(response, user.id,db=db)




@router.get("/{skill_id}",response_model=SingleAssessmentResponse)
def get_assessment(skill_id:int, db:Session = Depends(get_db), user:AuthenticateUser=Depends(authenticate_user)):
    
    #edit below to match the right permission 
    if not Permission.check_permission(user.permissions, "assessment.read"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User does not have permission to start assessments")

    single_assessment_instance,error = fetch_single_assessment(skill_id=skill_id,db=db)
    
    #check for corresponding errors
    if error:
        raise error
    if not single_assessment_instance:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Critical error occured while getting assessment details")
    response = {
        "assessment_id":single_assessment_instance.id,
        "skill_id": skill_id,
        "title": single_assessment_instance.title,
        "description" : single_assessment_instance.description,
        "duration_minutes" : single_assessment_instance.duration_minutes,
        "pass_score":single_assessment_instance.pass_score,
        "status": single_assessment_instance.status,
        "start_date": single_assessment_instance.start_date,
        "end_date": single_assessment_instance.end_date,
        }

    return response
