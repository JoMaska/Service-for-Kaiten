import aiohttp

async def make_request(url, method, data, headers):
    async with aiohttp.ClientSession() as session:
        async with session.request(url=url, method=method, json=data, headers=headers) as response:
            print('\nMake request : \n',url, method, data, headers)
            return await response.json()
