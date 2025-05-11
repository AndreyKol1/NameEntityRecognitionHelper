from app.core.mongo import MongoDB
from app.core.ner import Ner
from fastapi import UploadFile
from app.handlers.response_handler import HTMLResponseHandler, JSONResponseHandler


class MongoService:
    def __init__(self):
        self.db = MongoDB()
        self.ner = Ner()
        self.html_handler = HTMLResponseHandler()
        self.json_handler = JSONResponseHandler()
        
    
    async def load_json(self, json_data: UploadFile, template, request):
        try:
            data = await json_data.read()
            preprocessed_data_json = self.ner.preprocessDataJson(data.decode("utf-8"))
            self.db.insert_data_from_json(preprocessed_data_json)
            
            return self.html_handler.success(request, template, message=" ", json_data=True)
        
        except Exception as e:
            return self.html_handler.error(request, template, str(e))
        
    async def drop_collection(self):
        try:
            self.db.delete_all_data()
            return self.json_handler.success({"message": "Data deleted successfully!"})
        
        except Exception as e:
            return self.json_handler.error(str(e))