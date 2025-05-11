from fastapi import APIRouter, Request
from app.services.page_service import PageService
from fastapi.responses import HTMLResponse

router = APIRouter()
page_service = PageService()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return page_service.render_homepage(request)

@router.get("/train", response_class=HTMLResponse)
async def train_page(request: Request):
    return page_service.render_train_page(request)

@router.get("/test", response_class=HTMLResponse)
async def inference_page(request: Request):
    return page_service.render_inference_page(request)
