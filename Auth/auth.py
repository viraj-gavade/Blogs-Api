import os
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from fastapi import status
from utils.imports import * 



pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')



def hash_password(plain_password : str)-> str :
    return pwd_context.hash(plain_password)


def decodeToken(token : str):
    try:
        paylod = jwt.decode(token,SECRETE_KEY,algorithms=[ALGORITHM])
        return paylod
    
    except JWTError:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= {'message':'JWT ERROR','Error': JWTError}
        )


def create_access_token(payload : dict):
    try:
        payload = payload.copy()
        accessToken = jwt.encode(payload,SECRETE_KEY)
        return accessToken
    
    except JWTError:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= {'message':'JWT ERROR','Error': JWTError}
        )
    
def verifyPassword(user_pass:str,db_pass:str)->bool:
    return pwd_context.verify(user_pass,db_pass)
