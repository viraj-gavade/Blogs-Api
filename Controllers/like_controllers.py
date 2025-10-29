
from fastapi import Depends
from DataBase.connect import ConnectDB
from Midddlewares.auth_middleware import verifyJWT
from Models.sql_models import BlogModel
from Models.sql_models import LikeModel
from sqlalchemy.orm import Session

def toggleBlogLike(id : int ,  db : Session = Depends(ConnectDB) , current_user = Depends(verifyJWT) ):
    if not current_user :
        return 'Not Authenticated'
    blog = db.query(BlogModel).filter(BlogModel.id==id).first()
    if not blog:
        return 'Blog does not exists'
    existing_like = db.query(LikeModel).filter(
        LikeModel.Blog_id == blog.id,
        LikeModel.LikedBy == current_user['id']
    ).first()
    if not existing_like:
        new_like = LikeModel(
            Blog_id = blog.id,
            LikedBy = current_user['id']
        )
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        return 'Blog Liked '
  
    db.delete(existing_like)
    db.commit()
    return 'Blog UnLiked '
    
    



