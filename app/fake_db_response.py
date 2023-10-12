from app.response_schemas import UserAssessmentResponse, UserAssessment, Question, Assessment
User = {
    "id": 1,  # Object count (can be used as a unique identifier within the sample)
    "user_id": "e4c56a27-2f6d-4d58-a6fc-914f28b6aa3a",  # A UUID representing the user's unique identifier
    "username": "john_doe",  # The username of the user
    "first_name": "John",  # The first name of the user
    "last_name": "Doe",  # The last name of the user
    "email": "john.doe@example.com",  # The email address of the user
    "password": "hashed_password",  # The hashed password of the user
    "section_order": "section1,section2,section3",  # The order of sections (as a string)
    "provider": "local",  # The authentication provider (e.g., "local" for local authentication)
    "profile_pic": "profile_pic_url",  # URL to the user's profile picture
    "refresh_token": "refresh_token_value",  # The user's refresh token
    "created_at": "2023-10-07T12:00:00.000Z",  # The timestamp when the user was created
    "updated_at": "2023-10-07T14:30:00.000Z"  # The timestamp when the user was last updated
}
# Sample data
UserAssessments = [
    {
        'id': 1,
        'user_id': 'e4c56a27-2f6d-4d58-a6fc-914f28b6aa3a',
        'assessment_id': 1,
        'score': 0.0,
        'status': 'pending',
        'submission_date': '2021-09-08T15:43:00.000Z',
        'assessment': {
            'id': 1,
            'title': 'Python Assessment',
            'description': 'This is a python assessment',
            'questions': [
                {
                    'id': 1,
                    'question_text': 'What is Python?',
                    'question_type': 'MCQ'
                },
                {
                    'id': 2,
                    'question_text': 'What is Python used for?',
                    'question_type': 'MCQ'
                },
                {
                    'id': 3,
                    'question_text': 'What is the difference between a list and a tuple?',
                    'question_type': 'MCQ'
                },
                # Include more questions here
            ]
        }
    },
    {
        'id': 2,
        'user_id': 'e4c56a27-2f6d-4d58-a6fc-914f28b6aa3a',
        'assessment_id': 2,
        'score': 0.0,
        'status': 'complete',
        'submission_date': '2021-09-09T16:15:00.000Z',
        'assessment': {
            'id': 2,
            'title': 'JavaScript Assessment',
            'description': 'This is a JavaScript assessment',
            'questions': [
                {
                    'id': 1,
                    'question_text': 'What is JavaScript?',
                    'question_type': 'MCQ'
                },
                # Include more questions here
            ]
        }
    },
    # Include more sample assessments
]


response_data = [
    {
        "id": 1,
        "user_id": "e4c56a27-2f6d-4d58-a6fc-914f28b6aa3a",
        "assessment_id": 123,
        "score": 85.5,
        "status": "complete",
        "submission_date": "2023-10-07T15:30:00Z",
        "assessment": {
            "id": 123,
            "skill_id": 456,
            "title": "Sample Assessment 1",
            "description": "This is a sample assessment 1.",
            "duration_minutes": 30,
            "pass_score": 80.0,
            "status": "active",
            "start_date": "2023-10-07T12:00:00Z",
            "end_date": "2023-10-07T12:30:00Z"
        }
    },
    {
        "id": 2,
        "user_id": "f7e89b35-1f45-4c6a-9b23-53a7b4a86a8d",
        "assessment_id": 456,
        "score": 70.0,
        "status": "complete",
        "submission_date": "2023-10-08T10:45:00Z",
        "assessment": {
            "id": 456,
            "skill_id": 789,
            "title": "Sample Assessment 2",
            "description": "This is a sample assessment 2.",
            "duration_minutes": 45,
            "pass_score": 75.0,
            "status": "active",
            "start_date": "2023-10-08T09:00:00Z",
            "end_date": "2023-10-08T09:45:00Z"
        }
    },
    {
        "id": 3,
        "user_id": "d3e1c1a8-0ff3-4dce-a341-7f4c314af221",
        "assessment_id": 789,
        "score": 92.0,
        "status": "complete",
        "submission_date": "2023-10-09T14:15:00Z",
        "assessment": {
            "id": 789,
            "skill_id": 123,
            "title": "Sample Assessment 3",
            "description": "This is a sample assessment 3.",
            "duration_minutes": 60,
            "pass_score": 90.0,
            "status": "active",
            "start_date": "2023-10-09T13:00:00Z",
            "end_date": "2023-10-09T14:00:00Z"
        }
    }
]

#use this information to test run the start assessment endpoint
#user_id:e4c56a27-2f6d-4d58-a6fc-914f28b6aa3a,assessment_id:111
#user_id:f7e89b35-1f45-4c6a-9b23-53a7b4a86a8d,assessment_id:456
#user_id:d3e1c1a8-0ff3-4dce-a341-7f4c314af221,assessment_id:789

Questions =[
    {
    "assessment_id":111,
    "id":1,
    "question_text":"This is a sample question and this is question 1",
    "question_type":"obj",
    },
    {
    "assessment_id":111,
    "id":2,
    "question_text":"This is a sample question and this is question 2",
    "question_type":"obj",
    },
    {
    "assessment_id":111,
    "id":3,
    "question_text":"This is a sample question and this is question 3",
    "question_type":"theory",
    },
    {
    "assessment_id":111,
    "id":4,
    "question_text":"This is a sample question and this is question 4",
    "question_type":"theory",
    },
    {
    "assessment_id":456,
    "id":1,
    "question_text":"This is a sample question and this is question 1",
    "question_type":"MCQ",
    },
    {
    "assessment_id":456,
    "id":2,
    "question_text":"This is a sample question and this is question 2",
    "question_type":"MCQ",
    },
    {
    "assessment_id":456,
    "id":3,
    "question_text":"This is a sample question and this is question 3",
    "question_type":"MCQ",
    },
    {
    "assessment_id":789,
    "id":1,
    "question_text":"This is a sample question and this is question 5",
    "question_type":"MCQ",
    },
    {
    "assessment_id":789,
    "id":2,
    "question_text":"This is a sample question and this is question 1",
    "question_type":"MCQ",
    },
    {
    "assessment_id":789,
    "id":3,
    "question_text":"This is a sample question and this is question 2",
    "question_type":"MCQ",
    },
    {
    "assessment_id":789,
    "id":4,
    "question_text":"This is a sample question and this is question 3",
    "question_type":"MCQ",
    },
    {
    "assessment_id":789,
    "id":5,
    "question_text":"This is a sample question and this is question 4",
    "question_type":"MCQ",
    },

    
]


Answers =[
    {
    "question_id":1,
    "answer_text":"This is a sample answer and this is answer 1",
    },

    {
    "question_id":2,
    "answer_text":"This is a sample answer and this is answer 2",
    },

    {
    "question_id":3,
    "answer_text":"This is a sample answer and this is answer 3",
    },

    {
    "question_id":4,
    "answer_text":"This is a sample answer and this is answer 4",
    },

    {
    "question_id":5,
    "answer_text":"This is a sample answer and this is answer 5",
    },
    
        
]