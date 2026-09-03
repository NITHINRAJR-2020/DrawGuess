import jwt
from core.config import Config
from datetime import datetime , timedelta
from db.database import sessionLocal 

class auth_services():

    def create_jwt(username :str , user_id : int):
        expire=datetime.utcnow()+timedelta(minutes=30)
        payload={'sub':username , 'id':user_id , 'exp':expire}
        return jwt.encode(payload,Config.JWT_SECRET,algorithm=Config.JWT_ALGORITHMALGORITHM)



db_dependency=Annotated[Session,Depends(get_db)]







def cookie_jwt(request:Request):
    token=request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token



async def decode_jwt(token : Annotated[str,Depends(cookie_jwt)]):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username=payload.get("sub")
        user_id=payload.get("id")
        expires=payload.get("exp")
        if not username or not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
        return{"username":username, "user_id":user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)    
