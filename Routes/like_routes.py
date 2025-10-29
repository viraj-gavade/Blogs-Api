from fastapi import APIRouter
from Controllers.like_controllers import *
from fastapi import Depends
from DataBase.connect import ConnectDB
from Midddlewares.auth_middleware import verifyJWT
LikeRouter = APIRouter()



@LikeRouter.get('/toggle/{id}')
def like(id : int ,  db : Session = Depends(ConnectDB) , current_user = Depends(verifyJWT)):
    return toggleBlogLike(id , db , current_user)




