import aiohttp

session_pool = aiohttp.ClientSessionPool()

async def make_request(url, method='GET', data=None, headers=None):
    session = await session_pool.acquire()
    async with session.request(url=url, method=method, data=data, headers=headers) as response:
        return await response.json()
    session_pool.release(session)
