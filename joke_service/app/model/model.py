from pydantic import BaseModel
from typing import Optional

class Joke(BaseModel):
    id: Optional[int]
    content: str
    category: Optional[str]
