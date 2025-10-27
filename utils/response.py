
from fastapi.responses import JSONResponse

from fastapi.responses import JSONResponse

class CustomResponse:
    @staticmethod
    def success(message: str, status_code: int = 200, data: dict = None):
        response = {"status": "success", "message": message}
        if data:
            response["data"] = data
        return JSONResponse(content=response, status_code=status_code)

    @staticmethod
    def error(message: str, status_code: int = 400):
        response = {"status": "error", "message": message}
        return JSONResponse(content=response, status_code=status_code)
