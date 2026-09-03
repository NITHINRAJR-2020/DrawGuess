from sqlalchemy.ext.asyncio import AsyncSession
from db.models import UserModel


class UserServices():

    def authenticate(self , username:str,password:str,db:AsyncSession):
        db_data=db.query(UserModel).filter(UserModel.username==username).first()
        if not db_data:
            return False
        if not bycript_context.verify(password,db_data.password):
            return False
        
        return db_data