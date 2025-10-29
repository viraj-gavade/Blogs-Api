
from Schemas.comment_schemas import CommentSchema ,UpdateCommentSchema
from sqlalchemy.orm import Session
from fastapi import Depends
from DataBase.connect import ConnectDB
from Midddlewares.auth_middleware import verifyJWT
from Models.sql_models import CommentsModel
from Models.sql_models import BlogModel


def createComment(blog_id : int ,comment : CommentSchema , db : Session,curr_user = Depends(verifyJWT)):
    if not curr_user:
        return 'Not Authenticated'
    blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()
    if not blog :
        return 'Blog not found!'
    
    new_comment = CommentsModel(
        content = comment.content,
        Blog_id = blog_id,
        CommentedBy = curr_user['id']
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return 'Comment added successfully!'




def updateComment(comment_id : int ,comment : UpdateCommentSchema , db : Session,curr_user = Depends(verifyJWT)):
    if not curr_user:
        return 'Not Authenticated'
    existing_comment = db.query(CommentsModel).filter(CommentsModel.id == comment_id).first()
    if not existing_comment :
        return 'Comment not found!'
    else:
        if not existing_comment.CommentedBy == curr_user['id']:
            return 'Not Authenticated to delete this comment'
        else:
            new_comment = comment.model_dump(exclude_unset=True)
            for key , value in new_comment.items():
                setattr(existing_comment,key,value)

            db.commit()
            db.refresh(existing_comment)
            return 'Comment updated successfully!'



def deleteComment(comment_id : int , db : Session,curr_user = Depends(verifyJWT)):
    if not curr_user:
        return 'Not Authenticated'
    comment  = db.query(CommentsModel).filter(CommentsModel.id == comment_id).first()
    if not comment :
        return 'Comment  not found!'
    else:
        if not comment.CommentedBy == curr_user['id']:
            return 'Not Authenticated to delete this comment'
        else:
            db.delete(comment)
            db.commit()
            return 'Comment deleted successfully!'