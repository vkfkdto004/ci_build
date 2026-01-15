# 답변을 DB에 저장하기 위한 answer_crud
from datetime import datetime
from sqlalchemy.orm import Session
from domain.answer.answer_schema import AnswerCreate
from models import Question, Answer

def create_answer(db: Session, question: Question, answer_create: AnswerCreate):
    db_answer = Answer(question=question, content=answer_create.content, create_date=datetime.now())
    db.add(db_answer)
    db.commit()

