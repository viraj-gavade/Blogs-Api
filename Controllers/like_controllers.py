
from fastapi import Depends
from DataBase.connect import ConnectDB
from Midddlewares.auth_middleware import verifyJWT
from Models.sql_models import BlogModel
from Models.sql_models import LikeModel
from sqlalchemy.orm import Session
from utils.response import CustomResponse
from fastapi import status
from fastapi.encoders import jsonable_encoder

def toggleBlogLike(id : int ,  db : Session = Depends(ConnectDB) , current_user = Depends(verifyJWT) ):
    if not current_user :
        return CustomResponse.error(
            message=' Not Authenticated ! ',
            status_code= status.HTTP_401_UNAUTHORIZED
        )
    blog = db.query(BlogModel).filter(BlogModel.id==id).first()
    if not blog:
        return CustomResponse.error(
            message=' Blog Not Found ! ',
            status_code= status.HTTP_404_NOT_FOUND
        )
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
        return CustomResponse.success(
            message=' Blog Liked Successfully! ',
            status_code= status.HTTP_200_OK
        )
  
    db.delete(existing_like)
    db.commit()
    return CustomResponse.success(
            message=' Blog UnLiked Successfully! ',
            status_code= status.HTTP_200_OK
        )
    
    



