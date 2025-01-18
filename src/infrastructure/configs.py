import os
from dynaconf import Dynaconf
from pydantic import BaseModel

class Tododdler(BaseModel):
        url: str

class KeyclockConfig(BaseModel):
    auth_url: str
    grant_type: str
    client_id: str
    client_secret: str
    secret_key: str

class SpacesConfig(BaseModel):
    spaces: dict

class Config(BaseModel):
    keyclock_config: KeyclockConfig
    spaces_config: SpacesConfig
    tododdler: Tododdler

def load_config():
    settings = Dynaconf(
        settings_files=[os.environ['CONFIG_PATH'],
                        os.environ['SECRETS_PATH'],
                        os.environ['SPACES_PATH']
                        ])

    config = Config(
            
        keyclock_config=KeyclockConfig(
                auth_url=settings["secrets"]["auth_url"],
                grant_type=settings["secrets"]["grant_type"],
                client_id=settings["secrets"]["client_id"],
                client_secret=settings["secrets"]["client_secret"],
                secret_key=settings["secrets"]["secret_key"]
                ),
        
        spaces_config=SpacesConfig(
                spaces=settings["spaces"],
                ),
        
        tododdler=Tododdler(
                url=settings["settings"]["tododdler_url"],
                ),
    )
    return config