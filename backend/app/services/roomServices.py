from schemas.room_schemas import RoomSchema
from db.session import get_db 
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.room_models import RoomModel

class RoomServices():
    async def create_room(self , room : RoomSchema , db : AsyncSession):


    