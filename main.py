from fastapi import FastAPI
from utils.response import CustomResponse
from DataBase.connect import engine
from Routes.auth_routes import AuthRouter
from Routes.user_routes import UserRouter
from Routes.blog_routes import BlogRouter
from Routes.like_routes import LikeRouter

import Models.sql_models

Models.sql_models.Base.metadata.create_all(engine)


app = FastAPI()

app.include_router(AuthRouter,prefix='/auth',tags=['auth'])
app.include_router(UserRouter,prefix='/user',tags=['user'])
app.include_router(BlogRouter,prefix='/blog',tags=['blog'])
app.include_router(LikeRouter,prefix='/like',tags=['Like'])



@app.get('/')
def get_home():
    return CustomResponse.success(
        message='Blogs Api Running Successfully!'
    )