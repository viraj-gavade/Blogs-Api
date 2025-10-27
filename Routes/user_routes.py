from fastapi import APIRouter
from Controllers.user_controllers import *
from Midddlewares.auth_middleware import verifyJWT
from fastapi import Depends
from DataBase.connect import ConnectDB
from sqlalchemy.orm import Session
from Schemas.user_schemas import UserPublic

UserRouter = APIRouter()


@UserRouter.get('/me')
def me(db : Session = Depends(ConnectDB),current_user = Depends(verifyJWT)):
    return get_user(db,current_user)


@UserRouter.put('/me/update')
def update(user : UpdateUser ,db : Session = Depends(ConnectDB),current_user = Depends(verifyJWT)):
    return update_user(user , db , current_user)



@UserRouter.get('/me/comments')
def comments(db : Session = Depends(ConnectDB),current_user = Depends(verifyJWT)):
    return get_my_comments( db , current_user)


@UserRouter.get('/me/likes')
def comments(db : Session = Depends(ConnectDB),current_user = Depends(verifyJWT)):
    return get_my_likes( db , current_user)


@UserRouter.get('/me/blogs')
def comments(db : Session = Depends(ConnectDB),current_user = Depends(verifyJWT)):
    return get_my_blogs( db , current_user)