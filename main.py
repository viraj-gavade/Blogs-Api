from fastapi import FastAPI
from utils.response import CustomResponse



app = FastAPI()


@app.get('/')
def get_home():
    return CustomResponse.success(
        message='Blogs Api Running Successfully!'
    )