from pydantic import BaseModel
from typing import List, Optional


class User(BaseModel):
    user_id: int
    user_name: str
    powers: str


class Tool(BaseModel):
    id: int
    name: str


class BoxDetection(BaseModel):
    box_id: str
    predicted_class: str
    confidence: float
    possible_tools: List[str]


class Work(BaseModel):
    request_id: int
    user_id: int
    set_id: int
    state: str
    photo_ids_giving: Optional[List[str]]
    photo_ids_getting: Optional[List[str]]
