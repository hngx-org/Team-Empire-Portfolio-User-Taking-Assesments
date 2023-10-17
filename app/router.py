from fastapi import APIRouter, HTTPException, status, Depends,Request, Response, Header,BackgroundTasks
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
from app.services.assessment import get_assessment_results,get_completed_assessments
from app.schemas import StartAssessment, UserAssessmentQuery, UserAssessmentanswer
from app.response_schemas import StartAssessmentResponse, UserAssessmentResponse, Questions,SingleAssessmentResponse
from app.services.user_session import  save_session,send_email
from app.config import Permission, settings
from app.services.external import fake_authenticate_user, authenticate_user, fetch_questions
from app.response_schemas import AuthenticateUser
from starlette.responses import RedirectResponse
from app.models import UserAssessment

# if settings.ENVIRONMENT == "development":
#     authenticate_user = fake_authenticate_user

# Create a router object
router = APIRouter(tags=["Assessments"], prefix="/assessments")


@router.get("" )
async def get_all_user_assessments(token:str = Header(...), db: Session = Depends(get_db)):
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
                        "title": "Python Assessment",
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

    user = authenticate_user(token=token, permission="assessment.read")
    # user = fake_authenticate_user()

    assessments, err = get_user_assessments_from_db(user_id=user.id, db=db)

    if err:
        raise err

    if not assessments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="failed to fetch assessments")

    response = {
        "message": "Assessments fetched successfully",
        "status_code": 200,
        "assessments": assessments
    }

    return response


@router.post("/start-assessment",)
async def start_assessment( request:StartAssessment,response:Response, token:str = Header(...), db:Session = Depends(get_db),):
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
    user = authenticate_user(token=token, permission="assessment.update.own")
    # user = fake_authenticate_user()

    assessment_id = request.assessment_id

    #check for assessment to get duration and set cookie
    assessment_instance,err = check_for_assessment(assessment_id=assessment_id,db=db)

    #check for corresponding matching id
    if err:
        raise err

    if not assessment_instance:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Critical error occured while getting assessment details")


    #get all questions for the assessment
    questions_instance,error = fetch_questions(assessment_id=assessment_id,db=db, count=False)

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
            question_no=question.question_no or 0,
            question_text=question.question_text ,
            question_type=question.question_type ,
            answer_id=question.answer.id,
            options=question.answer.options
            ))

    is_user_assessment = db.query(UserAssessment).filter(UserAssessment.user_id==user.id,UserAssessment.assessment_id==assessment_id).first()

    if not is_user_assessment:
        user_assessment = UserAssessment(
            user_id=user.id,
            assessment_id=assessment_id,
            score=0,
            status="pending",
            time_spent=0,
            submission_date=None
        )

        db.add(user_assessment)
        db.commit()
        db.refresh(user_assessment)


    return {
        "message": "Assessment started successfully",
        "status_code": 200,
        "data": {
            "questions": question_list
        }
    }


@router.get("/session/{assessment_id}")
async def get_session_details(assessment_id:int, response:Request,token:str = Header(...),db:Session = Depends(get_db),):

    user = authenticate_user(token=token, permission="assessment.update.own")
    # user = fake_authenticate_user()
    #get assessment id from cookie



    unanswered_question, answered_question, error = fetch_answered_and_unanswered_questions(assessment_id=assessment_id, user_id=user.id,db=db)

    if error:
        raise error

    if not unanswered_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Assessment already completed")

    answered_question_list = []
    unanswered_question_list = []

    if answered_question != []:

        for question in answered_question:
            answered_question_list.append(Questions(
                question_id=question.question_id,
                question_no=question.question.question_no,
                question_text=question.question.question_text,
                question_type=question.question.question_type,
                answer_id=question.answer_id or 0,
                options=question.answer.options,
                user_selected_answer= question.selected_response,
                ))

    if unanswered_question != []:

        for question in unanswered_question:
            unanswered_question_list.append(Questions(
                question_id=question.id,
                question_no=question.question_no or 0,
                question_text=question.question_text,
                question_type=question.question_type,
                answer_id=question.answer.id,
                options=question.answer.options
                ))

    return {
        "message": "Session details fetched successfully",
        "status_code": 200,
        "data": {
            "answered_questions": answered_question_list,
            "unanswered_questions": unanswered_question_list
        }
    }

@router.get("/{assessment_id}/result", status_code=200)
async def get_assessment_result(
    assessment_id: int,
    token:str = Header(...),
    db: Session = Depends(get_db),

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
    user = authenticate_user(token=token, permission="assessment.read")

    score, assessment_status, answers = get_assessment_results(user_id=user.id, assessment_id=assessment_id, db=db)

    response = {
        "score": score,
        "user_id": user.id,
        "assessment_id": assessment_id,
        "status": assessment_status,
        "answers": answers
    }

    return response

@router.post("/submit", )
async def submit_assessment(
    background_task:BackgroundTasks,response:UserAssessmentanswer, db: Session = Depends(get_db),token:str = Header(...)
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
    user = authenticate_user(token=token, permission="assessment.update.own")
    # user = fake_authenticate_user()

    # check if user is eligible to submit assessment at first if required
    # user_id comes from auth

    return save_session(response, user.id,db=db, background_task=background_task)



@router.get('/get-user-assessments')
def get_user_completed_assessments(token:str = Header(...),db:Session = Depends(get_db)):
    user = authenticate_user(token=token, permission="assessment.read")
    # user=fake_authenticate_user()
    completed_assessments,error=get_completed_assessments(user.id,db=db)
    if error:
        raise error
    return completed_assessments





@router.get("/{skill_id}")
def get_assessment(skill_id:int, token:str = Header(...),db:Session = Depends(get_db),):

    user = authenticate_user(token=token, permission="assessment.read")
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

    question_count, err = fetch_questions(assessment_id=single_assessment_instance.id,db=db, count=True)

    if err:
        raise err

    if not question_count:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Critical error occured while getting assessment details")

    response = {
        "assessment_id":single_assessment_instance.id,
        "skill_id": skill_id,
        "title": single_assessment_instance.title,
        "description" : single_assessment_instance.description,
        "duration_minutes" : single_assessment_instance.duration_minutes,
        "question_count": question_count,
        "status": single_assessment_instance.status,
        "start_date": single_assessment_instance.start_date,
        "end_date": single_assessment_instance.end_date,
        }

    return response


