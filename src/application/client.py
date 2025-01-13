import io
import logging
from typing import Any, List
from cryptography.fernet import Fernet

import aiohttp
from fastapi import HTTPException, Request, UploadFile
from infrastructure.aiohttp.aiohttp_session import SingletonAiohttp

logger = logging.getLogger(__name__)
    # try:
    #     response = await make_request(url, method='POST')
    #     logger.info('Получена конфигурация сервера')
    #     return response
    # except Exception as Error:
    #     raise HTTPException(status_code=500, detail=f"Ошибка при получении конфигурации Kaiten: {Error}")
    
    
    #client = httpx.Client()
    # response = client.post(
    #     auth_url,
    #     data={
    #         "grant_type": "client_credentials",
    #         "client_id": "some-client-id",
    #         "client_secret": decoder.decrypt("some-client-secret".encode()).decode(),
    #     }
    # )
    
    
    # from pprint import pprint

    # import httpx
    # from cryptography.fernet import Fernet
    # decoder = Fernet(key="PgKi9XHK7409xmwvhpzZQfuO2yekPQxtjmocjI1e6Fo=")
    # auth_url = "https://auth.bytes2b.ru/realms/Dev/protocol/openid-connect/token"
    # profile_url = "https://auth.bytes2b.ru/realms/Dev/users/profile"

    # client = httpx.Client()

    # """
    # {
    # "clientId": "tododdler-user-2b3a0776-6f98-4d77-9383-671b876750dd",
    # "clientSecret": "gAAAAABnf09JPKQezvwM4fGto0m-i75AMXoHGAP8vmwKWH1c8Ib7j1fO5WAQCXTtU8pFhlD4f6f-LJ2gsxzsMDmR4xoURHlaA3qkkQm-utq0jsJQwgEA3S0_CF4M6E8N3jwUPM6w3vYW"
    # }
    # """
    # response = client.post(
    #     auth_url,
    #     data={
    #         "grant_type": "client_credentials",
    #         "client_id": "tododdler-user-2b3a0776-6f98-4d77-9383-671b876750dd",
    #         "client_secret": decoder.decrypt("gAAAAABnf09JPKQezvwM4fGto0m-i75AMXoHGAP8vmwKWH1c8Ib7j1fO5WAQCXTtU8pFhlD4f6f-LJ2gsxzsMDmR4xoURHlaA3qkkQm-utq0jsJQwgEA3S0_CF4M6E8N3jwUPM6w3vYW".encode()).decode(),
    #     }
    # )
    # access_token = response.json()['access_token']
    # pprint(response.json())

    # response = client.get(
    #     "https://stage.bytes2b.ru/api/space",
    #     headers={
    #         "Content-Type": "application/json",
    #         "Authorization": f"Bearer {access_token}"
    #     }
    # )

    # pprint(response.status_code)
    # pprint(response.content)


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
        response = await SingletonAiohttp.make_request(url=f'{kaiten_url}/api/latest/cards/{bug_ticket_id}/files',
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
        response = await SingletonAiohttp.make_request(url=f'{kaiten_url}/api/latest/cards',
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
        response = await SingletonAiohttp.make_request(url=f'{kaiten_url}/api/latest/cards/{bug_ticket_id}/children',
                                  method='POST',
                                  json={"card_id": bug_ticket_id,},
                                  headers={"Authorization": f'Bearer {api_token}'},
                                  response_as_json=False)
        logger.info('Создан дочерний тикет')
        logger.info(response)
        return response # Тут проблема, ошибка рода "Ошибка при создании дочерней задачи Kaiten: 500, message='Attempt to decode JSON with unexpected mimetype: text/html; charset=utf-8', url='https://bytes2b.kaiten.ru/api/latest/cards/43903861/children'"
    except Exception as Error:
        raise HTTPException(status_code=400, detail=f"Ошибка при создании дочерней задачи Kaiten: {Error}")

async def create_space(
    url: str,
    title: str,
    api_token: str
):
    response = await SingletonAiohttp.make_request(
        url=f"{url}api/space",
        method="POST",
        json={"title": title},
        headers={"Authorization": f'Bearer {api_token}'})
    return response

async def create_board(
    url: str,
    space_id: int,
    title: str,
    api_token: str
):
    response = await SingletonAiohttp.make_request(
        url=f"{url}api/board",
        method="POST",
        json={"space_id": space_id, "title": title},
        headers={"Authorization": f'Bearer {api_token}'})
    return response