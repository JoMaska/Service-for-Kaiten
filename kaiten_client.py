import logging
from typing import Any, List

from fastapi import HTTPException, UploadFile
from request import make_request

logger = logging.getLogger(__name__)

async def get_kaiten_config() -> dict[str, Any]:
    
    try:
        response = await make_request('https://test.born-in-july.ru/api/settings', "GET", None, None)
        logger.info('Получена конфигурация сервера')
        logger.info(response)
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
        response = await make_request(url=f'{kaiten_url}/api/latest/cards/{bug_ticket_id}/files',
                           method='PUT',
                           headers={"Authorization": f'Bearer {api_token}'},
                           data={'card_id': bug_ticket_id, 'file': (file.filename, content)})
        logger.info('Добавлены файлы к багу')
        logger.info(response)
        return response # Тут проблема с files, ошибка рода "url обязательный"
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
        logger.info(response)
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
                                  headers={"Authorization": f'Bearer {api_token}'})
        logger.info('Создан дочерний тикет')
        logger.info(response)
        return response # Тут проблема, ошибка рода "json битый"
    except Exception as Error:
        logger.error(Error)
        raise HTTPException(status_code=400, detail=f"Ошибка при создании дочерней задачи Kaiten: {Error}")