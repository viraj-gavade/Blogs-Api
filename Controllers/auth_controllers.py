from Models.sql_models import UserModel
from DataBase.connect import ConnectDB
from fastapi import Depends
from Schemas.user_schemas import SignInUser , SignupUser 
from sqlalchemy.orm import Session
from utils.response import CustomResponse
from Auth.auth import verifyPassword ,create_access_token,hash_password
from fastapi import status
from fastapi.responses import Response





def login_user(login_user : SignInUser ,response : Response, db : Session = Depends(ConnectDB) ,  ):
    db_user = db.query(UserModel).filter(UserModel.username == login_user.username).first()
    if not db_user:
         return CustomResponse.error(
            message='Invalid Username or password !',
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    isPasswordCorrect : bool = verifyPassword(login_user.password,db_user.password)
    if isPasswordCorrect == False:
        return CustomResponse.error(
            message='Invalid Username or password !',
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    payload : dict = {
        'id': db_user.id,
        'username': db_user.username,
        'email':db_user.email,
        'Full Name':db_user.fullName
    }
    
    accessToken = create_access_token(payload)
    response.set_cookie(
        key='accessToken',
        value=accessToken,
        httponly=True,
        samesite='lax'
    )

    response.status_code = status.HTTP_200_OK
    response.body = CustomResponse.success(
        message='User Logged in successfully!',
        data=accessToken
    ).body

    return response


def logout_user(response : Response, db : Session = Depends(ConnectDB) ):
    response = CustomResponse.success(message='User Logged out successfully!')
    response.delete_cookie(key='accessToken')
    return response


def register_user(register_user : SignupUser ,db : Session = Depends(ConnectDB) ):
    if(db.query(UserModel).filter(UserModel.email == register_user.email).first()):
        return CustomResponse.error(
            message='Email Already in Use !',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    if(db.query(UserModel).filter(UserModel.username == register_user.username).first()):
        return CustomResponse.error(
            message='Username Already in Use !',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    new_user = UserModel(
        fullName = register_user.fullName,
        username = register_user.username,
        password = hash_password(register_user.password),
        email = register_user.email
    )

    db.add(new_user)
    db.commit()

    public_User : dict = {
        'username': register_user.username,
        'email':register_user.email,
        'Full Name':register_user.fullName
    }

    return CustomResponse.success(
        message='User Registered Successfully!',
        data=public_User,
        status_code=status.HTTP_201_CREATED
    )