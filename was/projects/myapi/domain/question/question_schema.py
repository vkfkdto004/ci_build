import datetime
from pydantic import BaseModel

class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    # default 는 모두 필수로 작성해야 함.
    # 필수 항목이 아니게 설정 -> subject: str | None = None
