
from fastapi import APIRouter
from Controllers.blog_controllers import *
from fastapi import Depends
from DataBase.connect import ConnectDB
from Midddlewares.auth_middleware import verifyJWT
from Schemas.blog_schemas import UpdateBlog
BlogRouter = APIRouter()


@BlogRouter.get('/')
def getAll(db : Session = Depends(ConnectDB)):
    return getAllBlogs(db)


@BlogRouter.post('/')
def create(blog : Blog , db : Session = Depends(ConnectDB), current_user = Depends(verifyJWT) ):
    print('This work here ')
    return createBlog(blog,db,current_user)


@BlogRouter.get('/{id}')
def getSingle(id : int , db : Session = Depends(ConnectDB)):
    return getSingleBlogById(id , db)


@BlogRouter.put('/{id}')
def update(id : int , blog : UpdateBlog,   db : Session = Depends(ConnectDB),current_user = Depends(verifyJWT)):
    return updateBlogById(id , blog , db , current_user)

@BlogRouter.delete('/{id}')
def delete(id : int , db : Session = Depends(ConnectDB),current_user = Depends(verifyJWT)):
    return deleteBlogById(id , db , current_user)





