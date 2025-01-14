import logging

from fastapi import FastAPI
from presentation import routers
from infrastructure.aiohttp.aiohttp_session import on_shutdown, on_start_up

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

def main():
    app = FastAPI(on_startup=[on_start_up], on_shutdown=[on_shutdown])
    app.include_router(routers.router)
    logger.info("App created")
    return app

if __name__ == '__main__':
    import uvicorn
    app = main()
    uvicorn.run(app, port=8080)