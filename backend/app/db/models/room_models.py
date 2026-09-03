from database import base
from sqlalchemy import Column , String , UUID , DateTime
import uuid

class RoomModel(base):
    __tablename__ = "Rooms"
    name = Column(String , unique= True) 
    password = Column(String)
    host_id = Column(UUID)
    status = Column(String)
    created_at = Column(DateTime , default = )




