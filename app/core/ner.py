from transformers import AutoTokenizer, AutoModelForTokenClassification, DataCollatorForTokenClassification, TrainingArguments, Trainer, pipeline
from datasets import Dataset
import json
from app.models.schemas_model import FormaData

class Ner:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
        self.data_collator = DataCollatorForTokenClassification(tokenizer=self.tokenizer)
        self.training_args = TrainingArguments(
          output_dir="bert_finetuned_ner",
          learning_rate=2e-5,
          num_train_epochs=2,
          weight_decay=0.01,
          save_strategy="epoch",
          report_to="none",)
      
        self.pipeline = None
      


    def convertProperFormat(self, keyword, word_ids, tokens, label, sentence):
        new_labels = []
        first_added = False
        current_word = None
        tokens = [i.lower() for i in tokens]
        key_word_tokenized = self.tokenizer.tokenize(keyword)
        label = label.upper()
        
        if keyword.lower() not in sentence:
          raise ValueError(f"Keyword {keyword} not found in the sentence")

        for i, word_id in enumerate(word_ids):
          if word_id is None:
            new_labels.append(-100)
            continue

          elif word_id != current_word:
            if tokens[i] in key_word_tokenized:
              first_added = True
              new_labels.append(f"B-{label}")
            else:
              new_labels.append("O")
            current_word = word_id

          elif word_id == current_word:
            if tokens[i] in key_word_tokenized:
              if not first_added:
                first_added = True
                new_labels.append(f"B-{label}")
              else:
                new_labels.append(f"I-{label}")
            else:
              new_labels.append("O")
            current_word = word_id
        

        return new_labels
        
    def preprocessData(self, data):
      data_to_insert = self.tokenizer(data.sentence)
      formatted = self.convertProperFormat(data.word, data_to_insert.word_ids(), data_to_insert.tokens(), data.label, data.sentence)
      data_to_insert["labels"] = formatted
      return data_to_insert
      
    def preprocessDataJson(self, data_json):
      data = json.loads(data_json)
      for document in data:
        forma_data = FormaData(**document)
        yield self.preprocessData(forma_data)
      
      
    def train_model(self, data):
      clean_data = [{k: v for k, v in doc.items() if k != "_id"} for doc in data]
      
      entity_types = set()
      
      for doc in clean_data:
          for item in doc["labels"]:
            if item != 'O' and item != -100:
              entity_type = item.split('-')[1]
              entity_types.add(entity_type)
              
      self.labels = ["O"]
      for entity in entity_types:
        self.labels.append(f"B-{entity}")
        self.labels.append(f"I-{entity}")

      label2id = {label: idx for idx, label in enumerate(self.labels)}
      id2label = {idx: label for label, idx in label2id.items()}
      
      for doc in clean_data:
        doc["labels"] = [label2id[label] if label != - 100 else -100 for label in doc["labels"]]
      
      data = Dataset.from_list(clean_data)
      
      model = AutoModelForTokenClassification.from_pretrained("bert-base-cased", num_labels=len(label2id),
                                                              id2label=id2label, label2id = label2id)
      
      trainer = Trainer(
            model = model,
            args = self.training_args,
            train_dataset = data,
            data_collator=self.data_collator)
      
      trainer.train()

      self.pipeline = pipeline("ner", model=trainer.model, tokenizer=self.tokenizer, aggregation_strategy="simple")
      
    def predict(self, sentence):
      if self.pipeline is None:
        raise Exception("Try training your models first")
      return self.pipeline.predict(sentence)