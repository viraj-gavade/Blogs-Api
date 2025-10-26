
from fastapi.responses import JSONResponse


class CustomResponse:
    @staticmethod
    def success(message: str, data: dict = None):
        response = {"status": "success", "message": message}
        if data:
            response["data"] = data
        return JSONResponse(status_code=200, content=response)

    @staticmethod
    def error(message: str, status_code: int = 400):
        response = {"status": "error", "message": message}
        return JSONResponse(status_code=status_code, content=response)