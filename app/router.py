from fastapi import APIRouter, Response, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.external import check_for_assessment,fetch_questions
from app.services.user_assessment import get_user_assessments_from_db
from app.schemas import StartAssessment, UserAssessmentQuery
from app.response_schemas import StartAssessmentResponse, UserAssessmentResponse


# Create a router object
router = APIRouter(tags=["Assessments"], prefix="/assessments")


@router.get("/", response_model=UserAssessmentResponse)
async def get_all_user_assessments(request:UserAssessmentQuery,db:Session = Depends(get_db)):
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
    user_id = request.user_id
    assessments = get_user_assessments_from_db(user_id=user_id, db=db)
    
    return assessments
  


@router.post("/start-assessment",response_model=StartAssessmentResponse)
async def start_assessment(request:StartAssessment,db:Session = Depends(get_db)):
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
    user_id = request.user_id
    assessment_id = request.assessment_id
    _,err = check_for_assessment(user_id=user_id,assessment_id=assessment_id,db=db)
    
    #check for corresponding matching id
    if err:
        raise err
    
    
    questions,err = fetch_questions(assessment_id=assessment_id,db=db)

    if err:
        raise err
    
    #extract question(id,text type) and append to questions list
    question_list =[]
    for question in questions:
        single_question = {
            "id": question.id,
            "question_text":question.question_text,
            "question_type":question.question_type
        }
        question_list.append(single_question)
         
    response = {
        "message": "questions fetched successfully",
        "status_code": status.HTTP_200_OK,
        "questions": questions,
    }
    return response


@router.get("/{assessment_id}/result", status_code=200, response_model=AssessmentResults)
async def get_assessment_result(
    assessment_id,
    user_id,
    db: Session = Depends(get_db)
):

    score, status, answers = await get_assessment_results(user_id=user_id, assessment_id=assessment_id, db=db)
    
    response = {
        "score": score,
        "status": status,
        "answers": answers
    }
    

    return response
