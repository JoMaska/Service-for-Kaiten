from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel


class CreateCardRequest(BaseModel):
    board_id: int
    title: str
    description: str
    deadline: str
    type: str

class CreateAttachment(BaseModel):
    url: str
    card_id: int
    file: UploadFile
    api_token: str

class CreateTicket(BaseModel):
    url: str
    board_id: int
    title: str
    description: str
    deadline: Optional[str]
    type: str
    api_token: str

class CreateSpace(BaseModel):
    url: str
    title: str
    api_token: str
    
class CreateBoard(BaseModel):
    url: str
    space_id: int
    title: str
    api_token: str
    
class CreateChild(BaseModel):
    url: str
    card_id: int
    api_token: str