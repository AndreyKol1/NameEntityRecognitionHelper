from app.handlers.response_handler import HTMLResponseHandler, JSONResponseHandler
from transformers import AutoTokenizer, AutoModelForTokenClassification, DataCollatorForTokenClassification, TrainingArguments, Trainer, pipeline
from app.models.schemas_model import FormaData
from app.core.mongo import MongoDB
from fastapi import Form
from typing import Annotated
from app.core.ner import Ner
from fastapi.encoders import jsonable_encoder


class NERService:
    def __init__(self):
        self.ner = Ner()
        self.db = MongoDB()
        self.html_handler = HTMLResponseHandler()
        self.json_handler = JSONResponseHandler()
        
    async def preprocess_form_data(self, data: Annotated[FormaData, Form()], request=None, template=None):
        try:
            preprocessed_data = self.ner.preprocessData(data)
            self.db.insert_data_from_fields(preprocessed_data)
            
            if request and template:
                return self.html_handler.success(
                    request,
                    template,
                    message="✅ Data added successfully!"
                )
            return self.json_handler.success({"message": "Data added successfully!"})
        
        except ValueError as e:
            if request and template:
                return self.html_handler.error(
                    request,
                    template,
                    str(e)
                )
            return self.json_handler.error(str(e), status_code=422)
                
    async def train_ner_model(self, request=None, template=None):
        try:
            data = self.db.retrieve_data()
            self.ner.train_model(list(data))
            
            if request and template:
                return self.html_handler.success(
                    request,
                    template,
                    message="Training finished successfully"
                )
            return self.json_handler.success({"message": "Model trained successfully!"}) 
                
        except Exception as e:
            if request and template:
                return self.html_handler.error(
                    request,
                    template,
                    str(e)
                )
            return self.json_handler.error(str(e), status_code=422)
        
    async def test_model(self, sentence: Annotated[str, Form()]):
        try:
            result = self.ner.predict(sentence)
            simplified = [{"word": r["word"], "entity": r["entity_group"]} for r in result]
            return self.json_handler.success(jsonable_encoder(simplified))
        
        except Exception as e:
            return self.json_handler.error(str(e))
        