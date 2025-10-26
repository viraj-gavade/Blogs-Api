from fastapi import APIRouter
from Controllers.auth_controllers import * 


AuthRouter = APIRouter()


@AuthRouter.post('/register')
def register():
    return register_user()


@AuthRouter.post('/login')
def login():
    return login_user()

@AuthRouter.get('/logout')
def logout():
    return logout_user()