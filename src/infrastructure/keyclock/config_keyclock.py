import logging
from typing import Any

from cryptography.fernet import Fernet
from fastapi import HTTPException

from infrastructure.aiohttp.aiohttp_session import SingletonAiohttp


logger = logging.getLogger(__name__)

async def get_config_keycloak(settings: dict[str, Any]) -> dict[str, Any]:
    try:
        decoder = Fernet(settings['secret_key'])
        
        data={
            "grant_type": "client_credentials",
            "client_id": settings['client_id'],
            "client_secret": decoder.decrypt(settings['client_secret'].encode()).decode(),
        }
        logger.debug("Attempt to get config")
        
        response = await SingletonAiohttp.make_request(url=settings['auth_url'], method='POST', data=data)
        response = response['access_token']
        
    except Exception as Error:
        raise HTTPException(status_code=500, detail=f"Error getting configuration: {Error}")
    else:
        logger.debug("Config received successfully")
        
        return response
