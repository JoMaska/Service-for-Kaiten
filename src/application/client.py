import logging
import aiohttp
import httpx
from typing import Any

from fastapi import HTTPException, UploadFile, status
from infrastructure.aiohttp.aiohttp_session import SingletonAiohttp
from .schemas import CreateAttachment, CreateTicket, CreateSpace, CreateBoard, CreateChild

logger = logging.getLogger(__name__)
    
async def create_attachment(
    attachment: CreateAttachment
    ) -> dict[str, Any]:
    
    try:    
        async with httpx.AsyncClient() as client:
                    content = await attachment.file.read()
                    response = await client.post(
                        f"{attachment.url}api/card/{attachment.card_id}/attachment",
                        headers={"Authorization": f"api-key {attachment.api_token}"},
                        files={"file": (attachment.file.filename, content)}
                    )
        
        return response.json()
    
    except aiohttp.ClientResponseError as Error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error when attaching file: {Error}")

async def create_ticket(
    ticket: CreateTicket) -> dict[str, Any]:
    
    try:
        response = await SingletonAiohttp.make_request(
                url=f"{ticket.url}api/card",
                method="POST",
                json={"board_id": ticket.board_id,
                        "title": ticket.title,
                        "description": ticket.description,
                        "deadline": ticket.deadline,
                        "type": ticket.type, },
                headers={"Authorization": f'api-key {ticket.api_token}'}
            )
        
        return response
    
    except aiohttp.ClientResponseError as Error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error when creating a ticket: {Error}")

async def create_space(
    space: CreateSpace
    ) -> dict[str, Any]:
    
    try:
        response = await SingletonAiohttp.make_request(
            url=f"{space.url}api/space",
            method="POST",
            json={"title": space.title},
            headers={"Authorization": f'api-key {space.api_token}'})
        
        return response
    
    except aiohttp.ClientResponseError as Error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error when creating a space: {Error}")

async def create_board(
    board: CreateBoard
    ) -> dict[str, Any]:
    
    try:
        response = await SingletonAiohttp.make_request(
            url=f"{board.url}api/board",
            method="POST",
            json={"space_id": board.space_id, "title": board.title},
            headers={"Authorization": f'api-key {board.api_token}'})
        
        return response
    
    except aiohttp.ClientResponseError as Error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error when creating a board: {Error}")

async def create_child(
    child: CreateChild
    ) -> dict[str, Any]:
    
    try:
        response = await SingletonAiohttp.make_request(
            url=f"{child.url}api/card/{child.card_id}/children",
            json={"card_id": child.card_id},
            method="POST",
            headers={"Authorization": f'api-key {child.api_token}'})
        
        return response
    
    except aiohttp.ClientResponseError as Error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error when creating a child: {Error}")        