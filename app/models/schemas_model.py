from pydantic import BaseModel

class FormaData(BaseModel):
    sentence : str
    word : str
    label : str