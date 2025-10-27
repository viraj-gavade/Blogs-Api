from Midddlewares.auth_middleware import verifyJWT
from fastapi import Depends
from DataBase.connect import ConnectDB
from sqlalchemy.orm import Session
from Models.sql_models import UserModel
from Schemas.user_schemas import UserPublic,UpdateUser
from Models.sql_models import CommentsModel , LikeModel , BlogModel

def get_user(db : Session = Depends(ConnectDB),current_user = Depends(verifyJWT)):
    if not current_user:
        return 'Invalid Acess Token'
    username = current_user["username"]
    user = db.query(UserModel).filter(UserModel.username == username ).first()
    if not user :
        return 'User not found'
    return  UserPublic.model_validate(user)


def update_user(user : UpdateUser ,db : Session = Depends(ConnectDB),current_user = Depends(verifyJWT) ):
    if not current_user :
        return 'Invalid access Token'
    username = current_user["username"]
    db_user = db.query(UserModel).filter(UserModel.username == username ).first()
    if not db_user :
        return 'User not found'
    
    update_data = user.model_dump(exclude_unset=True)

    for key , value in update_data.items():
        setattr(db_user,key,value)
    db.commit()
    db.refresh(db_user)
    return 'User updated successfully!'


def get_my_comments(db : Session = Depends(ConnectDB),current_user = Depends(verifyJWT)):
    if not current_user :
        return 'Invalid access Token'
    userId = current_user["id"]
    blogs = (
    db.query(BlogModel)
    .join(CommentsModel, BlogModel.id == CommentsModel.Blog_id)
    .filter(CommentsModel.CommentedBy == userId)
    .all()
)
    if not blogs:
     return   'User has not made any comments on any blogs'
    
    return blogs


def get_my_likes(db : Session = Depends(ConnectDB),current_user = Depends(verifyJWT)):
    if not current_user :
        return 'Invalid access Token'
    userId = current_user["id"]
    blogs = (
    db.query(BlogModel)
    .join(LikeModel, LikeModel.id == LikeModel.Blog_id)
    .filter(LikeModel.LikedBy == userId)
    .all()
)
    if not blogs:
     return    'User has not liked any blogs'
    
    return blogs

def get_my_blogs(db : Session = Depends(ConnectDB),current_user = Depends(verifyJWT)):
    if not current_user :
        return 'Invalid access Token'
    userId = current_user["id"]
    blogs = (db.query(BlogModel).filter(BlogModel.createdBy == userId).all())
    print(type(blogs))
    print(len(blogs))
    if len(blogs) == 0 :
       return  'User  has not created any blogs'
    else:
    
        return blogs