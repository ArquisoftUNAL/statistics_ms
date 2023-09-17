from pydantic import BaseModel, Field

class IdModel(BaseModel):
    id: str = Field(regex=r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')