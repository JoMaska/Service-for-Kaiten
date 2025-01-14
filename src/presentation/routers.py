from dataclasses import dataclass
import logging
from typing import AsyncIterable, Iterable, List
import aiohttp
from fastapi import APIRouter, Body, File, Form, HTTPException, Request, UploadFile
import httpx

from entities.models import Ticket, Space, Board
from infrastructure.configs import load_config
from application.client import create_attachment, create_attachment2, create_child, create_space, create_board, create_ticket
from infrastructure.keyclock.config_keyclock import get_config_keycloak

logger = logging.getLogger(__name__)

config = load_config()

router = APIRouter()

@router.post("/api/tickets")
async def create_tickets_endpoint(
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),):
    #ticket: Ticket = Form(...)):
    
    
    # url = config["settings"]["standart_url"]
    # async with httpx.AsyncClient() as client:
    #     response = await client.post(
    #         f"{url}/api/card/330/attachment",
    #         #headers={"Authorization": f"api-key {access_token}"},
    #         #files={"file": (file.filename, content)}
    #     )
    #     response.raise_for_status()
    # return {}
    # async with aiohttp.ClientSession() as session:
    #     attachment = await session.post(
    #     url=f"{url}/api/space",)
    #     #data = aiohttp.FormData()
    #     #data.add_field('file', io.BytesIO(content))
    #     #data.add_field("file", file.file)#, filename=file.filename)
    #     #logger.info(file.file)
    #     #logger.info(file.filename)
    #     #logger.info(data)
    #     #data.add_field("card_id", str(ticket_bug["id"]))

    #     #json={"card_id": card_id},
    #     #headers={"Authorization": f'Bearer {api_token}'},
    #     #data=data)
    # # attachment = await create_attachment(
    # #     url,
    # #     ticket_bug["id"],
    # #     #ticket.file,
    # #     file,
    # #     api_token,
    # #     )
    # return await attachment.text()
    
    
    boards_ids = [] # boards titles: JoMaskaBoard1, JoMaskaBoard2
    for space in config["spaces"].values():
        boards_ids.append(space["board_id"])
        
    logger.debug(boards_ids)  # [157, 158]
    
    url = config["settings"]["standart_url"]
    api_token = await get_config_keycloak(config["secrets"])
    #for board_id in boards_ids:
    ticket_bug = await create_ticket(
        url=url,
        board_id=157,
        title=title,
        description=description,
        deadline=None,
        type="bug",
        api_token=api_token,)
    
        #"test_title_jomaska1",
        #"test_description_jomaska1",
        #ticket.title,
        #ticket.description,
        #"test-deadline",
        
    ticket_card = await create_ticket(
        url=url,
        board_id=157,
        title=title,
        description=description,
        deadline=None,
        type="card",
        api_token=api_token,)
    
    logger.info(ticket_bug)
    logger.info(ticket_card)  
    
    attachment = await create_attachment(
        url=url,
        card_id=ticket_bug["id"],
        #ticket.file,
        file=file,
        api_token=api_token,)
    
    logger.info(attachment)
    
    ticket_child = await create_child(
        url=url,
        card_id=ticket_bug["id"],
        api_token=api_token)
    
    logger.info(ticket_child)
    
    return ticket_child


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
