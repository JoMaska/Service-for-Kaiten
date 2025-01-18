import logging
from fastapi import APIRouter, File, Form, UploadFile

from application.schemas import CreateAttachment, CreateChild, CreateTicket
from entities.schemas import Ticket, Board, Space
from infrastructure.configs import load_config
from application.client import create_attachment, create_board, create_child, create_space, create_ticket
from infrastructure.keyclock.config_keyclock import get_config_keycloak
from entities.constant import CardType
from application.process_client import process_ticket_bug

logger = logging.getLogger(__name__)

config = load_config()

router = APIRouter()

@router.post("/api/tickets")
async def create_tickets_endpoint(
    #ticket: Ticket = Form(...)):
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),):
    
    url = config["settings"]["standart_url"]
    response = await process_ticket_bug(Ticket(title=title, description=description, file=file))
    
    return {"ticket_url": f'{url}ticket/{response["id"]}'}

@router.post("/api/space")
async def create_space_endpoint(
    space: Space = Form(...)):
    
    logger.debug("Attempt to create space")
    
    url = config["settings"]["standart_url"]
    api_token = await get_config_keycloak(config["secrets"])
    response = await create_space(url, space.title, api_token)
    
    return response

@router.post("/api/board")
async def create_board_endpoint(
    board: Board = Form(...)):
    
    logger.debug("Attempt to create board")
    
    url = config["settings"]["standart_url"]
    api_token = await get_config_keycloak(config["secrets"])
    response = await create_board(url, board.space_id, board.title, api_token)
    
    return response
