import logging
import aiohttp
import httpx
from typing import Any

from fastapi import HTTPException, UploadFile, status
from infrastructure.aiohttp.aiohttp_session import SingletonAiohttp
from application.client import create_attachment, create_child, create_ticket
from entities.constant import CardType
from entities.schemas import Ticket
from infrastructure.configs import load_config
from infrastructure.keyclock.config_keyclock import get_access_token_config_keycloak
from .schemas import CreateAttachment, CreateTicket, CreateSpace, CreateBoard, CreateChild

logger = logging.getLogger(__name__)

config = load_config()

async def process_ticket_bug(
    ticket: Ticket
    ) -> dict[str, Any]:
    
    boards_ids = dict()
    for space in config["spaces"].values():
        boards_ids[space["board_id"]] = space["primary_key"]
    
    url = config["settings"]["standart_url"]
    api_token = await get_access_token_config_keycloak(config["secrets"])
    
    primary_tickets = list()
    
    for board_id, is_primary in boards_ids.items():
        ticket_bug = CreateTicket(
            url=url,
            board_id=board_id,
            title=ticket.title,
            description=ticket.description,
            deadline=None,
            type=CardType.BUG,
            api_token=api_token,)
        
        ticket_bug = await create_ticket(ticket_bug)
        
        if is_primary == "True":
            primary_tickets.append(ticket_bug)

        logger.debug(ticket_bug)
        
        ticket_card = CreateTicket(
            url=url,
            board_id=board_id,
            title=ticket.title,
            description=ticket.description,
            deadline=None,
            type=CardType.CARD,
            api_token=api_token,)
        
        ticket_card = await create_ticket(ticket_card)
        
        logger.debug(ticket_card)  
        
        attachment = CreateAttachment(
            url=url,
            card_id=ticket_bug["id"],
            file=ticket.file,
            api_token=api_token,)
        
        attachment = await create_attachment(attachment)
        
        logger.debug(attachment)
        
        child = CreateChild(
            url=url,
            card_id=ticket_bug["id"],
            api_token=api_token)
        
        ticket_child = await create_child(child)
        
        logger.debug(ticket_child)
        
    return primary_tickets[0]