import aiohttp

async def make_request(url, method='GET', data=None, headers=None):
    async with aiohttp.ClientSession() as session:
        async with session.request(url=url, method=method, data=data, headers=headers) as response:
            return await response.json()
