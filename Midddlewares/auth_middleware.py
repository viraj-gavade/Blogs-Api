from fastapi.requests import Request
from fastapi import HTTPException
from fastapi import status
from Auth.auth import decodeToken
from jose import jwt, JWTError

def verifyJWT(request : Request):
    print(request.cookies)
    accessToken = request.cookies.get('accessToken')
    if not accessToken:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'message':'Not Authenticated'}
        )
    
    try :
        payload = decodeToken(accessToken)
        return payload
    
    except JWTError:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= {'message':'JWT ERROR','Error': JWTError}
        )
