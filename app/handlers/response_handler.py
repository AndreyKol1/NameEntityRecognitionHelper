from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="app/templates/")

class HTMLResponseHandler:
    @staticmethod
    def success(request: Request, template: str, message: str, **kwargs):
        context = {"request": request, "success": message, **kwargs}
        return templates.TemplateResponse(template, context)
    
    @staticmethod
    def error(request: Request, template: str, error: str, **kwargs):
        context = {"request": request, "error": error, **kwargs}
        return templates.TemplateResponse(template, context)
    
class JSONResponseHandler:
    @staticmethod
    def success(data: dict, status_code: int = 200):
        return JSONResponse(content={"data": data, "status": "success"}, status_code=status_code)
    
    @staticmethod
    def error(error: str, status_code: int = 500):
        return JSONResponse(content={"error": error, "status": "success"}, status_code=status_code)