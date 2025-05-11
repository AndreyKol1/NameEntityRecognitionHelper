from app.handlers.response_handler import HTMLResponseHandler, JSONResponseHandler
from fastapi import Request



class PageService:
    def __init__(self):
        self.html_handler = HTMLResponseHandler()
    
    def render_homepage(self, request: Request):
        return self.html_handler.success(request, template="index.html", message=None)
    
    def render_train_page(self, request: Request):
        return self.html_handler.success(request, template="train_model.html", message=None)
    
    def render_inference_page(self, request: Request):
        return self.html_handler.success(request, template="inference.html", message=None)