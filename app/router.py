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
    Retrieve all assessments for a user.

    Method: GET
    Request: Token

    Response:

        - message: Message indicating the status of the request
        - status_code: Status code of the request
        - assessments: List of assessments the user can take based on their skills

    Error Response:

            - message: Message indicating the status of the request
            - status_code: Status code of the request

    Example request:
    
                curl -X GET "http://localhost:8000/api/assessments" -H  "accept: application/json"  

    Example response:

            {
            "message": "Assessments fetched successfully",
            "status_code": 200,
            "assessments": [
                    Assessment(
                        "id": 1,
                        "title": "Python Assessment",
                        "description": "Python assessment for beginners",
                        "skil_id": 1,
                        "duration_minutes": 60,
                        "status": "pending",
                        "start_date": "2021-05-01",
                        "end_date": "2021-05-30"
                    ),
                    Assessment(
                        "id": 2,
                        "title": "Python Assessment",
                        "description": "Python assessment for beginners",
                        "skil_id": 1,
                        "duration_minutes": 60,
                        "status": "pending",
                        "start_date": "2021-05-01",
                        "end_date": "2021-05-30"
                    )
                ]
            }

    Error response:

            {
            "detail": "Unauthorized",
            "status_code": 401
            }

    Error response:
    
            {
            "detail": "No track found for this user",
            "status_code": 404
            }

    Error response:

            {
            "detail": "No assessments found for this user",
            "status_code": 404
            }

    Error response:
    
            {
            "detail": "failed to fetch assessments",
            "status_code": 500
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
    Request_body: token, assessment_id

    Response:
    
                - message: Message indicating the status of the request
                - status_code: Status code of the request
                - questions: List of questions for the assessment

    Error Response:
    
                - message: Message indicating the status of the request
                - status_code: Status code of the request

    Example request:

                curl -X POST "http://localhost:8000/api/assessments/start-assessment" -H  "accept: application/json" -H  \
                "Content-Type: application/json" -d "{\"assessment_id\":1}"

    Example response:

                {
                "message": "Assessment started successfully",
                "status_code": 200,
                "data": {
                    questions: [
                    Questions(
                        "question_id": 1,
                        "question_no": 1,
                        "question_text": "What is python?",
                        "question_type": "single_choice",
                        "answer_id": 1,
                        "options": [
                                "Option 1",
                                "Option 2",
                                "Option 3",
                                "Option 4"
                            ]
                        )
                    ]
                }
            }

    Error response:
    
            {
            "detail": "Unauthorized",
            "status_code": 401
            }

    Error response:
        
            {
            "detail": "No assessment found for provided assessment_id ",
            "status_code": 404
            }

    Error response:
            
            {
            "detail": "No questions found under the assessment_idr",
            "status_code": 404
            }

    Error response:
                    
            {
            "detail": "Critical error occured while getting assessment details",
            "status_code": 500
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
    """
    Retrieve session details for a user.

    Method: GET
    Request: Token, Assessment ID

    Response:
    
            - message: Message indicating the status of the request
            - status_code: Status code of the request
            - data: List of answered and unanswered questions for the assessment

    Error Response:
        
                - message: Message indicating the status of the request
                - status_code: Status code of the request
    
    Example request:
    
                curl -X GET "http://localhost:8000/api/assessments/session/1" -H  "accept: application/json" -H  \
                "Content-Type: application/json" -d "{\"assessment_id\":1}"
    
    Example response:
        
                {
                "message": "Session details fetched successfully",
                "status_code": 200,
                "data": {
                    "answered_questions": [
                        Questions(
                            "question_id": 1,
                            "question_no": 1,
                            "question_text": "What is python?",
                            "question_type": "single_choice",
                            "answer_id": 1,
                            "options": [
                                    "Option 1",
                                    "Option 2",
                                    "Option 3",
                                    "Option 4"
                                ],
                            "user_selected_answer": "Option 1"
                            )
                        ],
                    "unanswered_questions": [
                        Questions(
                            "question_id": 2,
                            "question_no": 2,
                            "question_text": "What is python?",
                            "question_type": "single_choice",
                            "answer_id": 2,
                            "options": [
                                    "Option 1",
                                    "Option 2",
                                    "Option 3",
                                    "Option 4"
                                ]
                            )
                        ]
                    }
                }

    Error response:
            
            {
            "detail": "Unauthorized",
            "status_code": 401
            }

    Error response:
                    
            {
            "detail": "Assessment already completed",
            "status_code": 400
            }

    """
    user = authenticate_user(token=token, permission="assessment.update.own")
    # user = fake_authenticate_user()
    #get assessment id from cookie



    unanswered_question, answered_question, error = fetch_answered_and_unanswered_questions(assessment_id=assessment_id, user_id=user.id,db=db)

    if error:
        raise error



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
    Request_body: Token, Assessment ID, Answers, time_spent, question_ID

    Response:
    
        - message: Message indicating the status of the request
        - status_code: Status code of the request

    Error Response:
    
        - message: Message indicating the status of the request
        - status_code: Status code of the request

    Example request:
        
        curl -X POST "http://localhost:8000/api/assessments/submit" -H  "accept: application/json" -H  \
        "Content-Type: application/json" -d "{\"assessment_id\":1,\"is_submitted\":true,\"time_spent\":60,\"response\":{\"question_id\":1,\"user_answer_id\":1}}"

    Example response:
            
            {
            "message": "Assessment submitted successfully",
            "status_code": 200
            }

    Error response:
                
            {
            "detail": "Unauthorized",
            "status_code": 401
            }

    Error response:
                            
            {
            "detail": "Assessment already completed",
            "status_code": 400
            }

    """
    user = authenticate_user(token=token, permission="assessment.update.own")
    # user = fake_authenticate_user()

    # check if user is eligible to submit assessment at first if required
    # user_id comes from auth

    return save_session(response, user.id,db=db, background_task=background_task, token= token)



@router.get('/get-user-assessments')
def get_user_completed_assessments(token:str = Header(...),db:Session = Depends(get_db)):

    """
    Retrieve all completed assessments for a user.

    Method: GET
    Request: Token

    Response:
    
        - message: Message indicating the status of the request
        - status_code: Status code of the request
        - assessments: List of assessments the user has completed

    Error Response:
        
        - message: Message indicating the status of the request
        - status_code: Status code of the request

    Example request:

        curl -X GET "http://localhost:8000/api/assessments/get-user-assessments" -H  "accept: application/json"

    Example response:
    
            {
            "message": "Completed assessments fetched successfully",
            "status_code": 200,
            "assessments": [
            {
                "id": 1,
                "user_id": 345-345mnb-345,
                "assessment_id": 1,
                "assessment_name": "Python Assessment",
                "skill_id": 1,
                "score": 10.0,
                "status": "complete",
                "submission_date": "2021-05-01",
                "badge_id": 1,
                "badge_name": "Intermediate"
            }
        ]

    Error response:

            {
            "detail": "Unauthorized",
            "status_code": 401
            }

    Error response:

            {
            "detail": "No assessments found for this user",
            "status_code": 404
            }

    """
    user = authenticate_user(token=token, permission="assessment.read")
    # user=fake_authenticate_user()
    completed_assessments,error=get_completed_assessments(user.id,db=db)
    if error:
        raise error
    return completed_assessments





@router.get("/{skill_id}")
def get_assessment(skill_id:int, token:str = Header(...),db:Session = Depends(get_db),):
    """
    Retrieve assessment details for an assessment.

    Method: GET
    Request: Token, Skill ID

    Response:

        - assessment_id: ID of the assessment
        - skill_id: ID of the skill
        - title: Title of the assessment
        - description: Description of the assessment
        - duration_minutes: Duration of the assessment
        - question_count: Number of questions in the assessment
        - status: Status of the assessment
        - start_date: Start date of the assessment
        - end_date: End date of the assessment

    Error Response:
    
        - message: Message indicating the status of the request
        - status_code: Status code of the request

    Example request:

        curl -X GET "http://localhost:8000/api/assessments/1" -H  "accept: application/json"

    Example response:
    
            {
            "assessment_id": 1,
            "skill_id": 1,
            "title": "Python Assessment",
            "description": "Python assessment for beginners",
            "duration_minutes": 60,
            "question_count": 10,
            "status": "pending",
            "start_date": "2021-05-01",
            "end_date": "2021-05-30"
            }

    Error response:
    
            {
            "detail": "Unauthorized",
            "status_code": 401
            }

    Error response:
                        
            {
            "detail": "No questions found under the assessment_id",
            "status_code": 404
            }

    """

    user = authenticate_user(token=token, permission="assessment.read")
    #edit below to match the right permission
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


