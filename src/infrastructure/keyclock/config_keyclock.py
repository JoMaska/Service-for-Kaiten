import logging

import aiohttp
from cryptography.fernet import Fernet
from fastapi import HTTPException, status

from infrastructure.aiohttp.aiohttp_session import SingletonAiohttp
from infrastructure.configs import Config
from .schemas import KeyclockData, KeyclockConfig

logger = logging.getLogger(__name__)

async def get_access_token_config_keycloak(config: Config) -> str:
    try:
        decoder = Fernet(config.keyclock_config.secret_key)
        
        data = KeyclockData(
            grant_type=config.keyclock_config.grant_type,
            client_id=config.keyclock_config.client_id,
            client_secret=decoder.decrypt(config.keyclock_config.client_secret.encode()).decode(),
        )
        data_dict = data.model_dump()
        
        logger.debug("Attempt to get config")
        
        response = await SingletonAiohttp.make_request(url=config.keyclock_config.auth_url, method=aiohttp.hdrs.METH_POST, data=data_dict)
        response = KeyclockConfig(access_token=response['access_token'])
        
        logger.debug("Config received successfully")
        
        return response.access_token
    
    except aiohttp.ClientResponseError as Error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error getting configuration: {Error}")
