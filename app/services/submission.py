from sqlalchemy.orm import Session
from app.models import Question,Answer,Assessment
from app.fake_db_response import Questions,Answers,Assessments


# create user_response table entry

def get_assessment(id,db:Session):
    # assessment=db.query(Assessment).filter(Assessment.id==id).first()
    assessment=[i for i in Assessments if i["id"]==id]
    return assessment

def check_correct(db:Session,question_id,ans_txt):
    # replace with query in prod
    # question=db.query(Answer).filter(Answer.question_id==question_id).first()
    question=[i for i in Questions if i["id"]==question_id][0]
    correct_answer=[i for i in question["answers"] if i["is_correct"]==True][0]
    print(correct_answer)
    if ans_txt == correct_answer["answer_text"]:
        return True
    else:
        return False
