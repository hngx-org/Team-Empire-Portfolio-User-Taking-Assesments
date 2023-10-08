UserAssessments = [
    {
        "id": 1,
        "user_id": "e4c56a27-2f6d-4d58-a6fc-914f28b6aa3a",
        "assessment_id": 123,
        "score": 85.5,
        "status": "complete",
        "submission_date": "2023-10-07T15:30:00Z"
    },
    {
        "id": 2,
        "user_id": "f7e89b35-1f45-4c6a-9b23-53a7b4a86a8d",
        "assessment_id": 456,
        "score": 70.0,
        "status": "complete",
        "submission_date": "2023-10-08T10:45:00Z"
    },
    {
        "id": 3,
        "user_id": "d3e1c1a8-0ff3-4dce-a341-7f4c314af221",
        "assessment_id": 789,
        "score": 92.0,
        "status": "complete",
        "submission_date": "2023-10-09T14:15:00Z"
    },
    {
        "id": 4,
        "user_id": "a1b2c3d4-e5f6-7890-1a2b-3c4d5e6f7890",
        "assessment_id": 101,
        "score": 78.5,
        "status": "pending",
        "submission_date": "2023-10-10T09:30:00Z"
    },
    {
        "id": 5,
        "user_id": "x1y2z3w4-v5u6-7890-1d2e-3f4g5h6i7890",
        "assessment_id": 222,
        "score": 60.0,
        "status": "failed",
        "submission_date": "2023-10-11T16:20:00Z"
    },
     {
        "id": 6,
        "user_id": "e4c56a27-2f6d-4d58-a6fc-914f28b6aa3a",
        "assessment_id": 111,
        "score": 0.0,
        "status": "pending",
        "submission_date": "2023-10-07T15:30:00Z"
    },
     {
        "id": 7,
        "user_id": "e4c56a27-2f6d-4d58-a6fc-914f28b6aa3a",
        "assessment_id": 127,
        "score": 30.5,
        "status": "failed",
        "submission_date": "2023-10-07T15:30:00Z"
    },
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