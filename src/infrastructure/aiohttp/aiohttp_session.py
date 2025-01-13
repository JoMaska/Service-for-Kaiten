import logging
from typing import Any, Optional

import aiohttp
from fastapi import HTTPException

logger = logging.getLogger(__name__)

# class SingletonAiohttp:
#         session: Optional[aiohttp.ClientSession] = None

#     @classmethod
#     def get_session(cls) -> aiohttp.ClientSession:
#         if session is None:
#             logging.info("Сессия создалась")
#             async with aiohttp.ClientSession() as session:
#                 cls._session = session
#         return cls._session

#     @classmethod
#     def make_request(cls,
#                         url: str,
#                         method: str="GET",
#                         json: dict[str, Any]=None,
#                         headers: dict[str, str]=None,
#                         data: aiohttp.FormData=None,
#                         title: str=None) -> Any:
#         session: aiohttp.ClientSession = cls._get_session()
#         #try:
#         async with session.request(url=url, method=method, json=json, headers=headers, data=data, title=title) as response:
#             response.raise_for_status()
#             logging.info("Запрос отправлен")
#             #if response.status != 200:
#                 #return {"ERROR OCCURED" + str(await response.text())}
#             json_result = await response.json()
#         #except Exception as e:
#         #    return {"ERROR": e}
#         return json_result
# async def make_request(
#     request: Request,
#     url: str,
#     method: str="GET",
#     json: dict[str, Any]=None,
#     headers: dict[str, str]=None,
#     data: aiohttp.FormData=None,
#     title: str=None
#     ) -> dict[str, Any]:
    
#     session = request.state.session
#     async with session.request(url=url, method=method, json=json, headers=headers, data=data, title=title) as response:
#         response.raise_for_status()
#         return await response.json()
class SingletonAiohttp:
    aiohttp_client: Optional[aiohttp.ClientSession] = None

    @classmethod
    def get_aiohttp_client(cls) -> aiohttp.ClientSession:
        if cls.aiohttp_client is None:
            #timeout = aiohttp.ClientTimeout(total=2)
            #connector = aiohttp.TCPConnector(family=AF_INET, limit_per_host=SIZE_POOL_AIOHTTP)
            #cls.aiohttp_client = aiohttp.ClientSession(timeout=timeout, connector=connector)
            cls.aiohttp_client = aiohttp.ClientSession()

        return cls.aiohttp_client

    @classmethod
    async def close_aiohttp_client(cls) -> None:
        if cls.aiohttp_client:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None

    @classmethod
    async def make_request(
        cls,
        url: str,
        method: str,
        json: dict[str, Any]=None,
        headers: dict[str, str]=None,
        data: aiohttp.FormData=None, ) -> dict[str, Any]:
        
        client = cls.get_aiohttp_client()
        try:
            async with client.request(url=url, method=method, json=json, data=data, headers=headers) as response:
                response.raise_for_status()
                json_result = await response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error while trying to make request: {e}")
        
        return json_result

async def on_start_up() -> None:
    logger.info("on_start_up")
    SingletonAiohttp.get_aiohttp_client()

async def on_shutdown() -> None:
    logger.info("on_shutdown")
    await SingletonAiohttp.close_aiohttp_client()