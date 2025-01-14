import logging
import httpx
from typing import Any

from fastapi import HTTPException, UploadFile
from infrastructure.aiohttp.aiohttp_session import SingletonAiohttp

logger = logging.getLogger(__name__)
    
async def create_attachment(
    url: str,
    card_id: id,
    file: UploadFile,
    api_token: str,
    ) -> dict[str, Any]:
    
    try:    
        async with httpx.AsyncClient() as client:
                    content = await file.read()
                    response = await client.post(
                        f"{url}api/card/{card_id}/attachment",
                        headers={"Authorization": f"api-key {api_token}"},
                        files={"file": (file.filename, content)}
                    )
                    response.raise_for_status() 
                    
    except Exception as Error:
        raise HTTPException(status_code=400, detail=f"Error when attaching file: {Error}")
    else:
        return response.json()

async def create_ticket(
    url: str,
    board_id: int,
    title: str,
    description: str,
    deadline: str,
    type: str,
    api_token: str
    ) -> dict[str, Any]:
    
    try:
        response = await SingletonAiohttp.make_request(
            url=f"{url}api/card",
            method="POST",
            json={"board_id": board_id,
                "title": title,
                "description": description,
                "deadline": deadline,
                "type": type, },
            headers={"Authorization": f'api-key {api_token}'})
        
    except Exception as Error:
        raise HTTPException(status_code=400, detail=f"Error when creating a ticket: {Error}")
    else:
        return response

async def create_space(
    url: str,
    title: str,
    api_token: str
    ) -> dict[str, Any]:
    
    try:
        response = await SingletonAiohttp.make_request(
            url=f"{url}api/space",
            method="POST",
            json={"title": title},
            headers={"Authorization": f'api-key {api_token}'})
        
    except Exception as Error:
        raise HTTPException(status_code=400, detail=f"Error when creating a space: {Error}")
    else:
        return response

async def create_board(
    url: str,
    space_id: int,
    title: str,
    api_token: str
    ) -> dict[str, Any]:
    
    try:
        response = await SingletonAiohttp.make_request(
            url=f"{url}api/board",
            method="POST",
            json={"space_id": space_id, "title": title},
            headers={"Authorization": f'api-key {api_token}'})
        
    except Exception as Error:
        raise HTTPException(status_code=400, detail=f"Error when creating a board: {Error}")
    else:
        return response

async def create_child(
    url: str,
    card_id: int,
    api_token: str
    ) -> dict[str, Any]:
    
    try:
        response = await SingletonAiohttp.make_request(
            url=f"{url}api/card/{card_id}/children",
            json={"card_id": card_id},
            method="POST",
            headers={"Authorization": f'api-key {api_token}'})
        
    except Exception as Error:
        raise HTTPException(status_code=400, detail=f"Error when creating a child: {Error}")
    else:
        return response