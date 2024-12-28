from typing import Any
import aiohttp
import logging

async def make_request(
    url: str,
    method: str="GET",
    json: dict[str, Any]=None,
    headers: dict[str, str]=None,
    data: aiohttp.FormData=None,
    #response_as_json: bool=True
    ) -> dict[str, Any]:
    
    async with aiohttp.ClientSession() as session:
        async with session.request(url=url, method=method, json=json, headers=headers, data=data) as response:
            #if response_as_json:
            response.raise_for_status()
            return await response.json()
            #else:
            #    response.raise_for_status()
            #    return response
