from database import base
from sqlalchemy import Column, Integer , String , ForeignKey

class User(base):
    __tablename__="userdata"

    id=Column(Integer , primary_key=True)
    username=Column(String)
    password=Column(String)