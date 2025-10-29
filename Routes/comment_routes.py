from fastapi import APIRouter
from Controllers.comment_controllers import *
from fastapi import Depends
from DataBase.connect import ConnectDB
from Schemas.comment_schemas import CommentSchema

CommentsRouter = APIRouter()


@CommentsRouter.post('/{blog_id}')
def add_comment(blog_id : int , comment : CommentSchema , db : Session = Depends(ConnectDB), curr_user = Depends(verifyJWT)):
    return createComment(blog_id,comment,db,curr_user)



@CommentsRouter.delete('/{comment_id}')
def delete_comment(comment_id : int , db : Session = Depends(ConnectDB),curr_user = Depends(verifyJWT)):
    return deleteComment(comment_id,db,curr_user)


@CommentsRouter.put('/{comment_id}')
def update_comment(comment_id : int , comment : UpdateCommentSchema ,db : Session = Depends(ConnectDB), curr_user = Depends(verifyJWT) ):
    return updateComment(comment_id,comment,db,curr_user)


