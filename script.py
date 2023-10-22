from app.database import get_db_unyield
from app.models import Answer, Question

questions_and_answer_list = [
    {
        "question_no": 1,
        "question_text": "Test Question 1",
        "question_type": "MCQ",
        "options": ["Test Option 1", "Test Option 2", "Test Option 3", "Test Option 4"],
        "correct_answer": "Test Option 1",
    },
    {
        "question_no": 2,
        "question_text": "Test Question 2",
        "question_type": "MCQ",
        "options": ["Test Option 1", "Test Option 2", "Test Option 3", "Test Option 4"],
        "correct_answer": "Test Option 2",
    },
    {
        "question_no": 3,
        "question_text": "Test Question 3",
        "question_type": "MCQ",
        "options": ["Test Option 1", "Test Option 2", "Test Option 3", "Test Option 4"],
        "correct_answer": "Test Option 3",
    },
    {
        "question_no": 4,
        "question_text": "Test Question 4",
        "question_type": "MCQ",
        "options": ["Test Option 1", "Test Option 2", "Test Option 3", "Test Option 4"],
        "correct_answer": "Test Option 4",
    },
    {
        "question_no": 5,
        "question_text": "Test Question 5",
        "question_type": "MCQ",
        "options": ["Test Option 1", "Test Option 2", "Test Option 3", "Test Option 4"],
        "correct_answer": "Test Option 1",
    },
    {
        "question_no": 6,
        "question_text": "Test Question 6",
        "question_type": "MCQ",
        "options": ["Test Option 1", "Test Option 2", "Test Option 3", "Test Option 4"],
        "correct_answer": "Test Option 2",
    },
    {
        "question_no": 7,
        "question_text": "Test Question 7",
        "question_type": "MCQ",
        "options": ["Test Option 1", "Test Option 2", "Test Option 3", "Test Option 4"],
        "correct_answer": "Test Option 3",
    },
    {
        "question_no": 8,
        "question_text": "Test Question 8",
        "question_type": "MCQ",
        "options": ["Test Option 1", "Test Option 2", "Test Option 3", "Test Option 4"],
        "correct_answer": "Test Option 4",
    },
    {
        "question_no": 9,
        "question_text": "Test Question 9",
        "question_type": "MCQ",
        "options": ["Test Option 1", "Test Option 2", "Test Option 3", "Test Option 4"],
        "correct_answer": "Test Option 1",
    },
    {
        "question_no": 10,
        "question_text": "Test Question 10",
        "question_type": "MCQ",
        "options": ["Test Option 1", "Test Option 2", "Test Option 3", "Test Option 4"],
        "correct_answer": "Test Option 2",
    },
]


def run():
    with get_db_unyield() as db:
        # user = db.query(User).filter(User.username == "testin").first()
        # track = db.query(Track).filter(Track.id == 6).first()
        # user_track = UserTrack(
        #   user_id=user.id,
        #   track_id=track.id,
        # )
        # db.add(user_track)
        # db.commit()
        # db.refresh(user_track)

        # create an assessment
        # assessment = db.query(Assessment).filter(Assessment.skill_id == 6).first()

        #   data = UserAssessment(
        #     user_id=user_.id,
        #     assessment_id=20,
        #     score=0,
        #     status="pending",
        #     time_spent=20,
        #     submission_date=datetime.now() + timedelta(days=2)
        #   )
        #   db.add(data)
        #   db.commit()
        #   db.refresh(data)

        #   # create questions and answer for the assessment
        for question_and_answer in questions_and_answer_list:
            question = Question(
                assessment_id=127,
                question_no=question_and_answer["question_no"],
                question_text=question_and_answer["question_text"],
                question_type=question_and_answer["question_type"],
            )
            db.add(question)
            db.commit()
            db.refresh(question)

            answer = Answer(
                question_id=question.id,
                options=question_and_answer["options"],
                correct_option=question_and_answer["correct_answer"],
            )
            db.add(answer)
            db.commit()
            db.refresh(answer)

    # create user response for the assessment
    # for question_and_answer in questions_and_answer_list:
    #   user_response = UserResponse(
    #     user_assessment_id=10,
    #     question_id=question.id,
    #     answer_id=answer.id,
    #     selected_text=question_and_answer.get("correct_answer")
    #   )
    #   db.add(user_response)
    #   db.commit()
    #   db.refresh(user_response)

    #   # populate user response for an assessment
    #   question = db.query(Question).filter(Question.assessment_id == 20).all()
    #   question_id = [q.id for q in question]
    #   answer_list = []
    #   for i in question_id:
    #     answer = db.query(Answer).filter(Answer.question_id == i).first()
    #     answer_list.append(answer)

    #   for i in answer_list:
    #     user_response = UserResponse(
    #       user_assessment_id=10,
    #       question_id=i.question_id,
    #       answer_id=i.id,
    #       selected_response=questions_and_answer_list[0].get("correct_answer")
    #     )
    #     db.add(user_response)
    #     db.commit()
    #     db.refresh(user_response)

    #   print("Done writing in database")
    #   print(f"assessment_id: {assessment.id}")
    #   print(f"user_id: {user_.id}")


if __name__ == "__main__":
    run()
