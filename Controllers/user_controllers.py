from Midddlewares.auth_middleware import verifyJWT
from fastapi import Depends
from DataBase.connect import ConnectDB
from sqlalchemy.orm import Session
from Models.sql_models import UserModel
from Schemas.user_schemas import UserPublic,UpdateUser,ChangePassword
from Models.sql_models import CommentsModel , LikeModel , BlogModel
from Auth.auth import verifyPassword ,hash_password
from utils.response import CustomResponse
from fastapi import status
from fastapi.encoders import jsonable_encoder

def get_user(db : Session = Depends(ConnectDB),current_user = Depends(verifyJWT)):
    if not current_user:
        return CustomResponse.error(
            message=' Not Authenticated ! ',
            status_code= status.HTTP_401_UNAUTHORIZED
        )
    username = current_user["username"]
    user = db.query(UserModel).filter(UserModel.username == username ).first()
    if not user :
        return CustomResponse.error(
            message='User Not Found!',
            status_code=status.HTTP_404_NOT_FOUND
        )
    return CustomResponse.success(
        message='User Profile fetched successfully!',
        data=jsonable_encoder(UserPublic.model_validate(user))
    )



def update_user(user : UpdateUser ,db : Session = Depends(ConnectDB),current_user = Depends(verifyJWT) ):
    if not current_user :
      return CustomResponse.error(
            message='Not Authenticated ! ',
            status_code= status.HTTP_401_UNAUTHORIZED
        )
    username = current_user["username"]
    db_user = db.query(UserModel).filter(UserModel.username == username ).first()
    if not db_user :
        return CustomResponse.error(
            message='User Not Found!',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    update_data = user.model_dump(exclude_unset=True)

    for key , value in update_data.items():
        setattr(db_user,key,value)
    db.commit()
    db.refresh(db_user)
    return CustomResponse.success(
        message='User Profile Updated Successfully!',
        status_code=status.HTTP_200_OK,
        data= jsonable_encoder(UserPublic.model_validate(db_user))
    )


def get_my_comments(db : Session = Depends(ConnectDB),current_user = Depends(verifyJWT)):
    if not current_user :
        return CustomResponse.error(
            message='Not Authenticated ! ',
            status_code= status.HTTP_401_UNAUTHORIZED
        )
    userId = current_user["id"]
    blogs = (
        db.query(BlogModel)
        .join(CommentsModel, BlogModel.id == CommentsModel.Blog_id)
        .filter(CommentsModel.CommentedBy == userId)
        .distinct()
        .all()
        )
    if not blogs:
     return  CustomResponse.error(
         message='"No comments found for this user.'
     )
    
    return CustomResponse.success(
        message= "User's commented blogs fetched successfully!",
        data= jsonable_encoder(blogs)
    )


def get_my_likes(db : Session = Depends(ConnectDB),current_user = Depends(verifyJWT)):
    if not current_user :
         return CustomResponse.error(
            message='Not Authenticated ! ',
            status_code= status.HTTP_401_UNAUTHORIZED
        )
    userId = current_user["id"]
    blogs = (
  db.query(BlogModel)
  .join(LikeModel, BlogModel.id == LikeModel.Blog_id)
  .filter(LikeModel.LikedBy == userId)
  .all()
    )

    if not blogs:
     return  CustomResponse.error(
         message='"No Likes found for this user.'
     )
    
    return CustomResponse.success(
        message= "User's Liked  blogs fetched successfully!",
        data=jsonable_encoder(blogs)
    )

def get_my_blogs(db : Session = Depends(ConnectDB),current_user = Depends(verifyJWT)):
    if not current_user :
        return CustomResponse.error(
            message='Not Authenticated ! ',
            status_code= status.HTTP_401_UNAUTHORIZED
        )
    userId = current_user["id"]
    blogs = (db.query(BlogModel).filter(BlogModel.createdBy == userId).all())
    if not blogs :
       return  CustomResponse.error(
         message='"No Blogs  found for this user.'
     )
    else:
        return CustomResponse.success(
        message= "User's   blogs fetched successfully!",
        data=jsonable_encoder(blogs)
    )
    

def change_password(
    passwords: ChangePassword,
    db: Session = Depends(ConnectDB),
    current_user=Depends(verifyJWT)
):
    if not current_user:
        return CustomResponse.error(
            message='Not Authenticated ! ',
            status_code= status.HTTP_401_UNAUTHORIZED
        )

    username = current_user["username"]
    user = db.query(UserModel).filter(UserModel.username == username).first()

    isPasscorrect = verifyPassword(passwords.current_pass, user.password)
    if not isPasscorrect:
        return  CustomResponse.error(
            message='Incorrect Cureent Password ! ',
            status_code= status.HTTP_401_UNAUTHORIZED
        )
    user.password = hash_password(passwords.new_password)
    db.commit()
    db.refresh(user)

    return CustomResponse.success(
        message= "User's   password updated successfully!",
        data= jsonable_encoder(UserPublic.model_validate(user))
    )
