from fastapi import APIRouter, Request, UploadFile, Form
from app.services.ner_service import NERService
from app.services.mongo_service import MongoService
from app.models.schemas_model import FormaData
from fastapi.responses import HTMLResponse
from typing import Annotated

router = APIRouter()
ner_service = NERService()
mongo_service = MongoService()

@router.post("/upload-json", response_class=HTMLResponse)
async def upload_json(json_data: UploadFile, request: Request):
    return await mongo_service.load_json(json_data, template="index.html", request=request)

@router.post("/drop_collection", response_class=HTMLResponse)
async def drop():
    return await mongo_service.drop_collection()

@router.post("/train", response_class=HTMLResponse)
async def train_model(request: Request):
    return await ner_service.train_ner_model(request=request, template="train_model.html")

@router.post("/", response_class=HTMLResponse)
async def add_entry(request: Request, data: Annotated[FormaData, Form()]):
    return await ner_service.preprocess_form_data(data, request=request, template="index.html")

@router.post("/test", response_class=HTMLResponse)
async def predict(sentence: Annotated[str, Form()]):
    return await ner_service.test_model(sentence)
