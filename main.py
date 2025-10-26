from fastapi import FastAPI
from utils.response import CustomResponse
from DataBase.connect import engine



import Models.sql_models

Models.sql_models.Base.metadata.create_all(engine)


app = FastAPI()



@app.get('/')
def get_home():
    return CustomResponse.success(
        message='Blogs Api Running Successfully!'
    )