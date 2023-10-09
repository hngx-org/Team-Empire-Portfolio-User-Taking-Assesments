from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.external import check_for_assessment,fetch_questions
from app.services.user_assessment import get_user_assessments_from_db
from app.services.assessment import get_assessment_results
from app.schemas import StartAssessment, UserAssessmentQuery
from app.response_schemas import StartAssessmentResponse, UserAssessmentResponse, AssessmentResults
from app.services.user_session import SessionData, get_all_session, get_session_detail, save_session
from app.config import Permission, settings
from app.services.external import fake_authenticate_user, authenticate_user
from app.response_schemas import AuthenticateUser

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
  


@router.post("/start-assessment",response_model=StartAssessmentResponse)
async def start_assessment(request:StartAssessment,db:Session = Depends(get_db),user=Depends(authenticate_user)):
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
    if not Permission.check_permission(user.permissions, "assessments::start"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User does not have permission to start assessments")
    
    user_id = request.user_id
    assessment_id = request.assessment_id
    _,err = check_for_assessment(user_id=user_id,assessment_id=assessment_id,db=db)
    
    #check for corresponding matching id
    if err:
        raise err
    
    #get all questions for the assessment
    questions_instance,error = fetch_questions(assessment_id=assessment_id,db=db)

    #check for availability of questions under the assessment_id
    if error:
        raise error
    if not questions_instance:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Critical error occured while fetching questions")
    
    #extract question(id,text type) and append to questions list
    #uncomment the block below after testing
    '''
    question_list =[]
    for question in questions_instance:
        single_question = {
            "id": question.id,
            "question_text":question.question_text,
            "question_type":question.question_type
        }
        question_list.append(single_question)
    '''
    question_list = questions_instance #comment this line after testing and grading
    response = {
        "message": "questions fetched successfully",
        "status_code": status.HTTP_200_OK,
        "questions": question_list,
    }
    return response


@router.get("/{assessment_id}/result", status_code=200, response_model=AssessmentResults)
async def get_assessment_result(
    assessment_id: int,
    user_id: str,
    db: Session = Depends(get_db),
    user=Depends(authenticate_user)
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
    if not Permission.check_permission(user.permissions, "results::view"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User does not have permission to view results")
    
    score, assessment_status, answers = get_assessment_results(user_id=user_id, assessment_id=assessment_id, db=db)
    
    response = {
        "score": score,
        "status": assessment_status,
        "answers": answers
    }
    

    return response

# @router.get("/user", response_model=List[UserAssessmentResponse])
# async def get_all_user_assessments(request:UserAssessmentQuery,db:Session = Depends(get_db), user=Depends(authenticate_user)):
#     """
#     Retrieve all assessments taken by a user.

#     Args:
#         db (Session): SQLAlchemy database session.
#         user_id (str): ID of the user whose assessments need to be retrieved.

#     Returns:
#         List[UserAssessment]: List of UserAssessment objects representing the assessments taken by the user.
#     """

#     if not Permission.check_permission(user.permissions, "assessments::view"):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail="User does not have permission to view assessments")
    
#     user_id = request.user_id
    
#      # Assuming you have a function to fetch a list of user assessments by user_id.
#     user_assessments = get_user_assessments_from_db(user_id=user_id, db=db)
#     if not user_assessments:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="User has no assessments")

#     return user_assessments

@router.post("/save_session/")
def save_endpoint(data: SessionData, user_id: int, user=Depends(authenticate_user)):
    """
    Saves the session data for a user.

    Method: POST
    Request_body: Session data

    Response:
    
            - message: Message indicating the status of the request
            - status_code: Status code of the request

    Error Response:
    
                - message: Message indicating the status of the request
                - status_code: Status code of the request

    Example request:

            curl -X POST "http://localhost:8000/api/assessments/save_session" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"user_id\":1,\"assessment_id\":1,\"answers\":[{\"question_id\":1,\"answer\":\"Python is a programming language\"},{\"question_id\":2,\"answer\":\"Python is used for web development\"},{\"question_id\":3,\"answer\":\"List is mutable\"},{\"question_id\":4,\"answer\":\"List is mutable\"},{\"question_id\":5,\"answer\":\"List is mutable\"},{\"question_id\":6,\"answer\":\"Set is mutable\"},{\"question_id\":7,\"answer\":\"Tuple is immutable\"},{\"question_id\":8,\"answer\":\"Tuple is immutable\"},{\"question_id\":9,\"answer\":\"Dictionary is mutable\"},{\"question_id\":10,\"answer\":\"List is mutable, Tuple is immutable, Dictionary is mutable, Set is mutable\"}]}"

    Example response:

            {
            "message": "Session saved successfully",
            "status_code": 200
            }

    Error response:

                {
                "message": "Assessment does not exist",
                "status_code": 404
                }
    """

    if not Permission.check_permission(user.permissions, "assessment::take"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User does not have permission to save session")
    # check if user is eligible to submit assessment at first if required
    # user_id comes from auth
    return save_session(data, user_id)

@router.get("/get_all_session/{user_id}")
def get_all_endpoint(user_id: int, user=Depends(authenticate_user)):

    """
    Retrieves all sessions for a user.

    Method: GET
    Request: User ID

    Response:
        
            - message: Message indicating the status of the request
            - status_code: Status code of the request
            - sessions: List of sessions for the user

    Error Response:

                - message: Message indicating the status of the request
                - status_code: Status code of the request

    Example request:

            curl -X GET "http://localhost:8000/api/assessments/get_all_session/1" -H  "accept: application/json"

    Example response:

            {
            "message": "Sessions fetched successfully",
            "status_code": 200,
            "sessions": [
                {
                    "id": 1,
                    "user_id": 1,
                    "assessment_id": 1,
                    "answers": [
                        {
                            "question_id": 1,
                            "answer": "Python is a programming language"
                        },
                        {
                            "question_id": 2,
                            "answer": "Python is used for web development"
                        },
                        {
                            "question_id": 3,
                            "answer": "List is mutable"
                        },
                        {
                            "question_id": 4,
                            "answer": "List is mutable"
                        },
                        {
                            "question_id": 5,
                            "answer": "List is mutable"
                        },
                        {
                            "question_id": 6,
                            "answer": "Set is mutable"
                        },
                        {
                            "question_id": 7,
                            "answer": "Tuple is immutable"
                        },
                        {
                            "question_id": 8,
                            "answer": "Tuple is immutable"
                        },
                        {
                            "question_id": 9,
                            "answer": "Dictionary is mutable"
                        },
                        {
                            "question_id": 10,
                            "answer": "List is mutable, Tuple is immutable, Dictionary is mutable, Set is mutable"
                        }
                    ]
                }
            ]

    Error response:
        
                    {
                    "message": "User does not exist",
                    "status_code": 404
                    }    
    """

    if not Permission.check_permission(user.permissions, "assessment::take"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User does not have permission to get all sessions")
    return get_all_session(user_id)

@router.get("/get_session_detail/{user_id}/{assessment_id}")
def get_detail_endpoint(user_id: int, assessment_id: int, user=Depends(authenticate_user)):
    """
    Retrieves session details for a user.

    Method: GET
    Request: User ID, Assessment ID

    Response:
            
                - message: Message indicating the status of the request
                - status_code: Status code of the request
                - session: Session details for the user

    Error Response:

                - message: Message indicating the status of the request
                - status_code: Status code of the request

    Example request:

            curl -X GET "http://localhost:8000/api/assessments/get_session_detail/1/1" -H  "accept: application/json"

    Example response:

            {
            "message": "Session fetched successfully",
            "status_code": 200,
            "session": {
                "id": 1,
                "user_id": 1,
                "assessment_id": 1,
                "answers": [
                    {
                        "question_id": 1,
                        "answer": "Python is a programming language"
                    },
                    {
                        "question_id": 2,
                        "answer": "Python is used for web development"
                    },
                    {
                        "question_id": 3,
                        "answer": "List is mutable"
                    },
                    {
                        "question_id": 4,
                        "answer": "List is mutable"
                    },
                    {
                        "question_id": 5,
                        "answer": "List is mutable"
                    },
                    {
                        "question_id": 6,
                        "answer": "Set is mutable"
                    },
                    {
                        "question_id": 7,
                        "answer": "Tuple is immutable"
                    },
                    {
                        "question_id": 8,
                        "answer": "Tuple is immutable"
                    },
                    {
                        "question_id": 9,
                        "answer": "Dictionary is mutable"
                    },
                    {
                        "question_id": 10,
                        "answer": "List is mutable, Tuple is immutable, Dictionary is mutable, Set is mutable"
                    }
                ]
            }
        }

    Error response:

                    {
                    "message": "Session does not exist",
                    "status_code": 404
                    }

    Error response:

                    {
                    "message": "User does not exist",
                    "status_code": 404
                    }
    """

    if not Permission.check_permission(user.permissions, "assessment::take"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User does not have permission to get session detail")
    
    # check if user is eligible to get details first. user_id comes from auth
    return get_session_detail(user_id, assessment_id)
