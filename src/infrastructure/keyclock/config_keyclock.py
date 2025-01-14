import logging
from typing import Any

from cryptography.fernet import Fernet

from infrastructure.aiohttp.aiohttp_session import SingletonAiohttp


logger = logging.getLogger(__name__)

async def get_config_keycloak(settings: dict[str, Any]) -> dict[str, Any]:
    decoder = Fernet(settings['secret_key'])
    
    data={
            "grant_type": "client_credentials",
            "client_id": settings['client_id'],
            "client_secret": decoder.decrypt(settings['client_secret'].encode()).decode(),
        }
    
    logger.debug("Attempt to get config")
    
    response = await SingletonAiohttp.make_request(url=settings['auth_url'], method='POST', data=data)
    response = response['access_token']
    
    logger.debug("Config received successfully")
    
    return response
