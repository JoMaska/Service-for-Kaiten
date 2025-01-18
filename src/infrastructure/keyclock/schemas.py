from pydantic import BaseModel

class KeyclockData(BaseModel):
    grant_type: str
    client_id: str
    client_secret: str

class KeyclockConfig(BaseModel):
    access_token: str