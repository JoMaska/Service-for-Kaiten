import io
import logging
from typing import Any, List

import aiohttp
from fastapi import HTTPException, UploadFile
from .request import make_request

logger = logging.getLogger(__name__)

async def get_kaiten_config(url) -> dict[str, Any]:
    
    try:
        response = await make_request(url)
        logger.info('Получена конфигурация сервера')
        return response
    except Exception as Error:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении конфигурации Kaiten: {Error}")

async def add_file_to_bug_ticket(
    kaiten_url: str,
    api_token: str,
    files: List[UploadFile],
    bug_ticket_id: id) -> dict[str, Any]:
    
    try:
        for file in files:
            content = await file.read()
        #data = aiohttp.FormData()
        #data.add_field('file', io.BytesIO(content))
        response = await make_request(url=f'{kaiten_url}/api/latest/cards/{bug_ticket_id}/files',
                           method='PUT',
                           headers={"Authorization": f'Bearer {api_token}'},
                           data={'file': (file.filename, content)})
                           #data={'file': data})
        logger.info('Добавлены файлы к багу')
        logger.info(response)
        response.raise_for_status()
        return response # Тут проблема с files, ошибка рода {'message': "File should have required property 'url'"}
    except Exception as Error:
       raise HTTPException(status_code=400, detail=f"Ошибка при приклеплении файла к баге Kaiten: {Error}")

async def create_bug_ticket(
    kaiten_url: str,
    api_token: str,
    board_id: id,
    title: str,
    description: str) -> dict[str, Any]:
    
    try:
        response = await make_request(url=f'{kaiten_url}/api/latest/cards',
                           method='POST',
                           json={'title': title, 'description': description, 'board_id': board_id},
                           headers={"Authorization": f'Bearer {api_token}'})
        logger.info('Создан тикет на багу')
        return response
    except Exception as Error:
        raise HTTPException(status_code=400, detail=f"Ошибка при создании баги Kaiten: {Error}")

async def create_task_ticket(
    kaiten_url: str,
    api_token: str,
    bug_ticket_id: id) -> dict[str, Any]:
    
    try:
        response = await make_request(url=f'{kaiten_url}/api/latest/cards/{bug_ticket_id}/children',
                                  method='POST',
                                  json={"card_id": bug_ticket_id,},
                                  headers={"Authorization": f'Bearer {api_token}'},
                                  response_as_json=False)
        logger.info('Создан дочерний тикет')
        logger.info(response)
        return response # Тут проблема, ошибка рода "Ошибка при создании дочерней задачи Kaiten: 500, message='Attempt to decode JSON with unexpected mimetype: text/html; charset=utf-8', url='https://bytes2b.kaiten.ru/api/latest/cards/43903861/children'"
    except Exception as Error:
        raise HTTPException(status_code=400, detail=f"Ошибка при создании дочерней задачи Kaiten: {Error}")