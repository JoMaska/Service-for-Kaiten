import logging
from fastapi import APIRouter, Body, File, Form, UploadFile

from entities.models import Board, Ticket, Space
from infrastructure.configs import load_config
from application.client import create_attachment, create_board, create_child, create_space, create_ticket
from infrastructure.keyclock.config_keyclock import get_config_keycloak

logger = logging.getLogger(__name__)

config = load_config()

router = APIRouter()

@router.post("/api/tickets")
async def create_tickets_endpoint(
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),):
    
    boards_ids = []
    board_id_for_return = []
    for space in config["spaces"].values():
        boards_ids.append(space["board_id"])
        if space["primary_key"] == "True":
            board_id_for_return.append(space["board_id"])
        
    logger.debug(boards_ids)
    
    url = config["settings"]["standart_url"]
    api_token = await get_config_keycloak(config["secrets"])
    
    for board_id in boards_ids:
        ticket_bug = await create_ticket(
            url=url,
            board_id=board_id,
            title=title,
            description=description,
            deadline=None,
            type="bug",
            api_token=api_token,)

        logger.debug(ticket_bug)
        
        ticket_card = await create_ticket(
            url=url,
            board_id=board_id,
            title=title,
            description=description,
            deadline=None,
            type="card",
            api_token=api_token,)
        
        logger.debug(ticket_card)  
        
        attachment = await create_attachment(
            url=url,
            card_id=ticket_bug["id"],
            file=file,
            api_token=api_token,)
        
        logger.debug(attachment)
        
        ticket_child = await create_child(
            url=url,
            card_id=ticket_bug["id"],
            api_token=api_token)
        
        logger.info(ticket_child)
    
    return {"ticket_url": f'{url}/ticket/{ticket_bug["id"]}'}

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
