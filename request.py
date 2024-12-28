from typing import Any
import aiohttp
import logging

async def make_request(
    url: str,
    method: str,
    json: dict[str, Any]=None,
    headers: dict[str, str]=None,
    data: aiohttp.FormData=None) -> dict[str, Any]:
    
    async with aiohttp.ClientSession() as session:
        async with session.request(url=url, method=method, json=json, headers=headers, data=data) as response:
            return await response.json()
