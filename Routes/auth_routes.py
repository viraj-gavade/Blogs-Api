from fastapi import APIRouter
from Controllers.auth_controllers import * 
from Schemas.user_schemas import SignInUser , SignupUser 
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.responses import Response
from DataBase.connect import ConnectDB


AuthRouter = APIRouter()


@AuthRouter.post('/register')
def register(user : SignupUser , db : Session = Depends(ConnectDB)):
    return register_user(user,db)


@AuthRouter.post('/login')
def login(user : SignInUser , response : Response , db : Session = Depends(ConnectDB)):
    return login_user(user,response,db)

@AuthRouter.get('/logout')
def logout(response : Response,):
    return logout_user(response)


