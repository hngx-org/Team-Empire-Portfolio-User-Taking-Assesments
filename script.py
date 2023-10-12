from app.database import get_db_unyield
from app.models import UserAssessment, Question, UserResponse, Answer, Assessment
from sqlalchemy.orm import Session
from datetime import datetime
from datetime import timedelta

questions_and_answer_list = [
  {
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

    # create an assessment 
    assessment = Assessment(
      skill_id=6, 
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


if __name__ == "__main__":
  run()