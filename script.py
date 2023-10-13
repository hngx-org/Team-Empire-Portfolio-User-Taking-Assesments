from app.database import get_db_unyield
from app.models import UserAssessment, Question, UserResponse, Answer, Assessment, User
from sqlalchemy.orm import Session
from datetime import datetime
from datetime import timedelta
from uuid import uuid4

questions_and_answer_list = [
  {
    "question_no":1,
    "question_text": "Test Question 1",
    "question_type": "MCQ",
    "options": [
      "Test Option 1",
      "Test Option 2",
      "Test Option 3",
      "Test Option 4"
    ],
    "correct_answer": "Test Option 1"
    },
  {
    "question_no":2,
    "question_text": "Test Question 2",
    "question_type": "MCQ",
    "options": [
      "Test Option 1",
      "Test Option 2",
      "Test Option 3",
      "Test Option 4"
    ],
    "correct_answer": "Test Option 2"
    },
  {
    "question_no":3,
    "question_text": "Test Question 3",
    "question_type": "MCQ",
    "options": [
      "Test Option 1",
      "Test Option 2",
      "Test Option 3",
      "Test Option 4"
    ],
    "correct_answer": "Test Option 3"
    },
  {
    "question_no":4,
    "question_text": "Test Question 4",
    "question_type": "MCQ",
    "options": [
      "Test Option 1",
      "Test Option 2",
      "Test Option 3",
      "Test Option 4"
    ],
    "correct_answer": "Test Option 4"
    },
  {
    "question_no":5,
    "question_text": "Test Question 5",
    "question_type": "MCQ",
    "options": [
      "Test Option 1",
      "Test Option 2",
      "Test Option 3",
      "Test Option 4"
    ],
    "correct_answer": "Test Option 1"
    },
  {
    "question_no":6,
    "question_text": "Test Question 6",
    "question_type": "MCQ",
    "options": [
      "Test Option 1",
      "Test Option 2",
      "Test Option 3",
      "Test Option 4"
    ],
    "correct_answer": "Test Option 2"
    },
  {
    "question_no":7,
    "question_text": "Test Question 7",
    "question_type": "MCQ",
    "options": [
      "Test Option 1",
      "Test Option 2",
      "Test Option 3",
      "Test Option 4"
    ],
    "correct_answer": "Test Option 3"
    },
  {
    "question_no":8,
    "question_text": "Test Question 8",
    "question_type": "MCQ",
    "options": [
      "Test Option 1",
      "Test Option 2",
      "Test Option 3",
      "Test Option 4"
    ],
    "correct_answer": "Test Option 4"
    },
  {
    "question_no":9,
    "question_text": "Test Question 9",
    "question_type": "MCQ",
    "options": [
      "Test Option 1",
      "Test Option 2",
      "Test Option 3",
      "Test Option 4"
    ],
    "correct_answer": "Test Option 1"
    },
  {
    "question_no":10,
    "question_text": "Test Question 10",
    "question_type": "MCQ",
    "options": [
      "Test Option 1",
      "Test Option 2",
      "Test Option 3",
      "Test Option 4"
    ],
    "correct_answer": "Test Option 2"
    }
]

def run():
  with get_db_unyield() as db:
    
    user_ = User(
      id = uuid4(),
      email="test@gmail.com",
      username="testin",
      first_name="tetrst",
      last_name="tesjhgt",
      password="teskhjgt",
      provider="google",
      section_order="test",
      createdAt=datetime.now(),
      profile_pic="test",
    )
    db.add(user_)
    db.commit()
    db.refresh(user_)

    data = UserAssessment(
      user_id=user_.id,
      assessment_id=20,
      score=0,
      status="pending",
      time_spent=20,
      submission_date=datetime.now() + timedelta(days=2)
    )
    db.add(data)
    db.commit()
    db.refresh(data)

    # create an assessment 
    assessment = Assessment(
      skill_id=9, 
      title = "Test Assessment",
      description = "Test Assessment Description",
      start_date = datetime.now(),
      duration_minutes = 30,
      status = "pending",
      end_date = datetime.now() + timedelta(days=1)
    )
      

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    # create questions and answer for the assessment
    for question_and_answer in questions_and_answer_list:
      question = Question(
        assessment_id=assessment.id,
        question_no = question_and_answer["question_no"],
        question_text=question_and_answer["question_text"],
        question_type=question_and_answer["question_type"]
        
      )
      db.add(question)
      db.commit()
      db.refresh(question)


      answer = Answer(
          question_id=question.id,
          options=question_and_answer["options"],
          correct_option = question_and_answer["correct_answer"]
        )
      db.add(answer)
      db.commit()
      db.refresh(answer)

    print("Done writing in database")
    print(f"assessment_id: {assessment.id}")



if __name__ == "__main__":
  run()