from fastapi import File, Form, UploadFile
from pydantic import BaseModel


class Ticket(BaseModel):
    title: str = Form(...)
    description: str = Form(...)
    file: UploadFile = File(...)
    
class Space(BaseModel):
    title: str = Form(...)
    
class Board(BaseModel):
    space_id: int = Form(...)
    title: str = Form(...)