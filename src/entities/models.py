from dataclasses import dataclass
from typing import List

from fastapi import UploadFile


@dataclass
class Ticket:
    title: str
    description: str
    files: List[UploadFile]
    
@dataclass
class Space:
    title: str
    
@dataclass
class Board:
    space_id: int
    title: str