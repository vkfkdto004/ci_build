from pydantic import BaseModel, field_validator

# 답변 등록 시 사용할 스키마로 AnswerCreate 클래스를 만들고, 답변 등록 시 파라미터는 content 하나고 string 타입으로 받음.
# content 속성은 디폴트 값이 없기 때문에 필숫값임.
class AnswerCreate(BaseModel):
    content: str

    # content는 필숫값이긴 하지만 ""와 같은 빈 문자열이 입력될 수 있는데, 이 빈문자열을 허용하지 않도록 설정.
    @field_validator('content')
    # 위 어노테이션 적용 후 not_empty 함수를 추가하여 AnswerCreate 스키마에 content 값이 저장될 때 마다 실행.
    def not_empty(cls, v):
        if not v or not v.strip():
            # content 값이 없거나, 빈 값인 경우 아래와 같은 오류가 발생.
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

# 답변 등록 API는 post 방식이고, content라는 입력 항목이 있다. 답변 등록 라우터에서 content 값을 읽기 위해서는 반드시 content 항목을 포함하는 pydantic 스키마를 통해서 읽어야한다.
# 스키마를 사용하지 않고 라우터 함수의 매개변수에 content: str을 추가하여 그 값을 읽기는 불가능. -> get이 아닌 다른 post, put, delete의 입력값은 pydantic 스키마로만 읽을 수 있다.
# 반대로 get 방식은 pydantic 스키마로 읽을 수 없고 각각 입력 항목을 라우터의 함수의 매개변수로 읽어야한다.

