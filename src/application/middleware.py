# import logging
# from typing import override
# import aiohttp
# from fastapi import HTTPException, Request
# from starlette.middleware.base import BaseHTTPMiddleware

# class SessionMiddlewaree(BaseHTTPMiddleware):
#     @override
#     async def dispatch(self, request: Request, call_next):
#         try:
#             async with aiohttp.ClientSession() as session:
#                 request.state.session = session
#                 response = await call_next(request)
#                 return response
#             logging.info("Мидлварь сработала")
#         except Exception as Error:
#             logging.error("Мидлварь не сработала")
#             raise HTTPException(status_code=500, detail=str(Error))