from pydantic import BaseModel

class MetaData(BaseModel):
    name: str
    phone: str
    latitude: float
    longitude: float