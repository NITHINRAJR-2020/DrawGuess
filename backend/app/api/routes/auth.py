from fastapi import APIRouter,Depends,Request , HTTPException
from fastapi.responses import RedirectResponse,HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
load_dotenv()
from starlette import status

from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import sessionLocal
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated,Dict
from jose import JWTError, jwt
from datetime import timedelta, datetime,timezone
import os
import db_models 
from models.user_models import user_model


router=APIRouter(prefix='/auth',tags=['auth'])

templates=Jinja2Templates(directory="templates")


SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

bycript_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer=OAuth2PasswordBearer(tokenUrl="/auth/login")
class Token(BaseModel):
    access_token:str
    token_type:str




@router.get('/',response_class=HTMLResponse)
def authpage(request:Request):
    return templates.TemplateResponse('login.html',{"request":request})

@router.post('/')
def signup(user:Annotated[OAuth2PasswordRequestForm,Depends()] , db:db_dependency):
    db_data=db_models.User(username=user.username , password=bycript_context.hash(user.password))
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    user_id=db_data.id
    jwt_token=create_jwt(user.username,user_id)

    response=RedirectResponse(
        url="/home",
        status_code=status.HTTP_302_FOUND
    )

    response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age="1800"
    )
    return response

@router.post('/login')
def login(formdata : Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    db_data=authenticate(formdata.username , formdata.password , db)
    if not db_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    jwt_token=create_jwt(db_data.username, db_data.id)
    response=RedirectResponse(
    url="/home",
    status_code=status.HTTP_302_FOUND
    )   

    response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age="1800"
    )
    return response





