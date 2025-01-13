from dataclasses import dataclass
import logging
from typing import AsyncIterable, Iterable, List
import aiohttp
from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile

from entities.models import Ticket, Space, Board
from infrastructure.configs import load_config
from application.client import create_space, create_board
from infrastructure.keyclock.config_keyclock import get_config_keycloak

logger = logging.getLogger(__name__)

config = load_config()

router = APIRouter()

@router.get("/api/tickets")
async def create_tickets_endpoint():
    #ticket: Ticket, ) -> dict[str, str]:
    
    logger.debug("Attempt to get config")
    response = await get_config_keycloak(config["secrets"])
    #response = await create_space(config["settings"]["standart_url"], "first_test_space_jomaska")
    #logging.info(ticket)
    return response
    # result = list()
    
    # for item in config['kaiten_urls']:
    #     kaiten_url = item['url']
    #     board_id = item['board_id']
    #     api_token = item['token']
    #     primary_key = item['primary']

    #     bug_ticket = await create_bug_ticket(kaiten_url, api_token, board_id, title, description)
    #     await add_file_to_bug_ticket(kaiten_url, api_token, files, bug_ticket['id'])
    #     await create_task_ticket(kaiten_url, api_token, bug_ticket['id'])

    #     if primary_key:
    #         result.append({"ticket_url": f'{kaiten_url}/ticket/{bug_ticket["id"]}'})

    # return result[0]
@router.post("/api/space")
async def create_space_endpoint(
    space: Space):
    logger.debug("Attempt to create space")
    url = config["settings"]["standart_url"]
    api_token = await get_config_keycloak(config["secrets"])
    response = await create_space(url, space.title, api_token)
    return response

@router.post("/api/board")
async def create_board_endpoint(
    board: Board):
    logger.debug("Attempt to create board")
    url = config["settings"]["standart_url"]
    api_token = await get_config_keycloak(config["secrets"])
    response = await create_board(url, board.space_id, board.title, api_token)
    return response
