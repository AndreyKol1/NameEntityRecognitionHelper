from fastapi import FastAPI
from app.routes import web_route, ner_route
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(web_route.router)
app.include_router(ner_route.router)
