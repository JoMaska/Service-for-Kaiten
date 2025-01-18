import logging
import aiohttp

from typing import Any, Optional

logger = logging.getLogger(__name__)

class SingletonAiohttp:
    aiohttp_client: Optional[aiohttp.ClientSession] = None

    @classmethod
    def get_aiohttp_client(cls) -> aiohttp.ClientSession:
        if cls.aiohttp_client is None:
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

        async with client.request(url=url, method=method, json=json, data=data, headers=headers) as response:
            json_result = await response.json()
    
        return json_result

async def on_start_up() -> None:
    logger.info("on_start_up")
    SingletonAiohttp.get_aiohttp_client()

async def on_shutdown() -> None:
    logger.info("on_shutdown")
    await SingletonAiohttp.close_aiohttp_client()