import os
from dynaconf import Dynaconf
# from pydantic import BaseModel

# # class KeyclockConfig(BaseModel):
# #     access_token: str

# class KeyclockConfig(BaseModel):
#     grant_type: str
#     client_id: str
#     client_secret: str
    
# class Config(BaseModel):
#     keyclock_config: KeyclockConfig

# # class KeyclockData(BaseModel):
# #     grant_type: str
# #     client_id: str
# #     client_secret: str

def load_config() -> Dynaconf:
        settings = Dynaconf(
            settings_files=[os.environ['CONFIG_PATH'],
                            os.environ['SECRETS_PATH'],
                            os.environ['SPACES_PATH']
                            ])
        
        return settings
    

# class KeyclockConfig(BaseModel):
#     auth_url: str
#     grant_type: str
#     client_id: str
#     client_secret: str

# class SpacesConfig(BaseModel):
#     spaces: dict

# class Config(BaseModel):
#     keyclock_config: KeyclockConfig
#     spaces_config: SpacesConfig

# def load_config():
#     settings = Dynaconf(
#         settings_files=[os.environ['CONFIG_PATH'],
#                         os.environ['SECRETS_PATH'],
#                         os.environ['SPACES_PATH']
#                         ])

#     config = Config(*settings)
#     return config