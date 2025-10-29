
from Schemas.comment_schemas import CommentSchema ,UpdateCommentSchema
from sqlalchemy.orm import Session
from fastapi import Depends
from DataBase.connect import ConnectDB
from Midddlewares.auth_middleware import verifyJWT
from Models.sql_models import CommentsModel
from Models.sql_models import BlogModel
from utils.response import CustomResponse
from fastapi import status
from fastapi.encoders import jsonable_encoder

def createComment(blog_id : int ,comment : CommentSchema , db : Session,curr_user = Depends(verifyJWT)):
    if not curr_user:
        return CustomResponse.error(
            message=' Not Authenticated ! ',
            status_code= status.HTTP_401_UNAUTHORIZED
        )
    blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()
    if not blog :
         return CustomResponse.error(
            message=' Blog Not Found ! ',
            status_code= status.HTTP_404_NOT_FOUND
        )
    
    new_comment = CommentsModel(
        content = comment.content,
        Blog_id = blog_id,
        CommentedBy = curr_user['id']
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return CustomResponse.success(
        message= 'Comment created successfully! ',
        status_code=status.HTTP_201_CREATED,
        data= jsonable_encoder(new_comment)
    )




def updateComment(comment_id : int ,comment : UpdateCommentSchema , db : Session,curr_user = Depends(verifyJWT)):
    if not curr_user:
        return CustomResponse.error(
            message=' Not Authenticated ! ',
            status_code= status.HTTP_401_UNAUTHORIZED
        )
    existing_comment = db.query(CommentsModel).filter(CommentsModel.id == comment_id).first()
    if not existing_comment :
        return CustomResponse.error(
            message=' Comment Not Found ! ',
            status_code= status.HTTP_404_NOT_FOUND
        )
    else:
        if not existing_comment.CommentedBy == curr_user['id']:
            return CustomResponse.error(
            message=' Not Authenticated ! ',
            status_code= status.HTTP_401_UNAUTHORIZED
        )
        else:
            new_comment = comment.model_dump(exclude_unset=True)
            for key , value in new_comment.items():
                setattr(existing_comment,key,value)

            db.commit()
            db.refresh(existing_comment)
            return CustomResponse.success(
            message= 'Comment updated successfully! ',
            status_code=status.HTTP_200_OK,
            data= jsonable_encoder(existing_comment)
    )



def deleteComment(comment_id : int , db : Session,curr_user = Depends(verifyJWT)):
    if not curr_user:
        return 'Not Authenticated'
    comment  = db.query(CommentsModel).filter(CommentsModel.id == comment_id).first()
    if not comment :
        return CustomResponse.error(
            message=' Comment Not Found ! ',
            status_code= status.HTTP_404_NOT_FOUND
        )
    else:
        if not comment.CommentedBy == curr_user['id']:
            return CustomResponse.error(
            message=' Not Authenticated ! ',
            status_code= status.HTTP_401_UNAUTHORIZED
        )
        else:
            db.delete(comment)
            db.commit()
            return CustomResponse.success(
            message= 'Comment Deleted successfully! ',
            status_code=status.HTTP_200_OK,
    )