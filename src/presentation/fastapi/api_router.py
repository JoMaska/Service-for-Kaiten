import logging
from typing import Any
from fastapi import APIRouter, File, Form, UploadFile

from application.schemas import CreateBoard, CreateSpace
from entities.schemas import Ticket, Board, Space
from infrastructure.configs import load_config
from application.client import create_board, create_space
from infrastructure.keyclock.config_keyclock import get_access_token_config_keycloak
from application.process_client import process_ticket_bug

logger = logging.getLogger(__name__)

config = load_config()

router = APIRouter()

@router.post("/api/tickets")
async def create_tickets_endpoint(
    #ticket: Ticket = Form(...)):
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
    ) -> dict[str, Any]:
    
    url = config["settings"]["standart_url"]
    response = await process_ticket_bug(Ticket(title=title, description=description, file=file))
    
    return {"ticket_url": f'{url}ticket/{response["id"]}'}

@router.post("/api/space")
async def create_space_endpoint(
    space: Space = Form(...)
    ) -> dict[str, Any]:
    
    logger.debug("Attempt to create space")
    
    url = config["settings"]["standart_url"]
    api_token = await get_access_token_config_keycloak(config["secrets"])
    response = await create_space(CreateSpace(url=url, title=space.title, api_token=api_token))
    
    return response

@router.post("/api/board")
async def create_board_endpoint(
    board: Board = Form(...)
    ) -> dict[str, Any]:
    
    logger.debug("Attempt to create board")
    
    url = config["settings"]["standart_url"]
    api_token = await get_access_token_config_keycloak(config["secrets"])
    response = await create_board(CreateBoard(url=url, space_id=board.space_id, title=board.title, api_token=api_token))
    
    return response
