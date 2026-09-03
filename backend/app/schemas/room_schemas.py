from pydantic import BaseModel
from datetime import datetime

class RoomSchema(BaseModel):
    name: str
    password: str
    host_id: str
    status: bool
    created_at: datetime