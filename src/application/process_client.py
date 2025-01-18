import logging
from typing import Any

from application.client import create_attachment, create_child, create_ticket
from entities.constant import CardType
from entities.schemas import Ticket
from infrastructure.configs import Config, load_config
from infrastructure.keyclock.config_keyclock import get_access_token_config_keycloak
from .schemas import CreateAttachment, CreateTicket, CreateChild, ProcessTicketBug

logger = logging.getLogger(__name__)

config = load_config()

async def process_ticket_bug(
    data: ProcessTicketBug
    ) -> dict[str, Any]:
    
    boards_ids = dict()
    
    spaces = data.config.spaces_config.model_dump()
    
    for space in spaces.values():
        for space_data in space.values():
            boards_ids[space_data["board_id"]] = space_data["primary_key"]
    
    primary_tickets = list()
    
    for board_id, is_primary in boards_ids.items():
        ticket_bug = CreateTicket(
            url=data.url,
            board_id=board_id,
            title=data.ticket.title,
            description=data.ticket.description,
            deadline=None,
            type=CardType.BUG,
            api_token=data.api_token,)
        
        ticket_bug = await create_ticket(ticket_bug)
        
        logger.debug(ticket_bug)
        
        if is_primary == "True":
            primary_tickets.append(ticket_bug)
        
        ticket_card = CreateTicket(
            url=data.url,
            board_id=board_id,
            title=data.ticket.title,
            description=data.ticket.description,
            deadline=None,
            type=CardType.CARD,
            api_token=data.api_token,)
        
        attachment = CreateAttachment(
            url=data.url,
            card_id=ticket_bug["id"],
            file=data.ticket.file,
            api_token=data.api_token,)
        
        child = CreateChild(
            url=data.url,
            card_id=ticket_bug["id"],
            api_token=data.api_token)
        

        ticket_card = await create_ticket(ticket_card)
        attachment = await create_attachment(attachment)
        ticket_child = await create_child(child)
        
        logger.debug(ticket_card) 
        logger.debug(attachment)
        logger.debug(ticket_child)
        
    logger.debug(primary_tickets)
    
    return primary_tickets[0]