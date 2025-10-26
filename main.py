from fastapi import FastAPI
from utils.response import CustomResponse
from DataBase.connect import engine
from Routes.auth_routes import AuthRouter

import Models.sql_models

Models.sql_models.Base.metadata.create_all(engine)


app = FastAPI()

app.include_router(AuthRouter,prefix='/auth',tags=['auth'])


@app.get('/')
def get_home():
    return CustomResponse.success(
        message='Blogs Api Running Successfully!'
    )