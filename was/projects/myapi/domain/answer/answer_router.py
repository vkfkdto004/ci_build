# 답변 등록 API
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.answer import answer_schema, answer_crud
from domain.question import question_crud

router = APIRouter(
    prefix="/api/answer",
)

# 입력 - answer_schema.AnswerCreate // 출력 - X
# 입력을 담당하는 AnswerCreate는 content 속성에 있고 프론트엔드에서 API 호출 시 파라미터로 전달한 content가 AnswerCreate 스키마에 자동으로 매핑
# 출력은 response_model 대신 status_code=status.HTTP_204_NO_CONTENT를 사용. (Error 204 --> No content)
@router.post("/create/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def answer_create(question_id: int, _answer_create: answer_schema.AnswerCreate, db: Session = Depends(get_db)):
    # 답변 생성
    question = question_crud.get_question(db, question_id=question_id)
    # 답변 등록을 하기 위해서 우선 question_id 값을 조회. 질문이 있어야 답변도 있는 법.
    # 답변이 없으면 Error 404, Question not found를 뱉어냄
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    answer_crud.create_answer(db, question=question, answer_create=_answer_create)




