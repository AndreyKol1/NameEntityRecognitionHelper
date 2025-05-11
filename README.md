# NER Helper

## Project information

**NER Helper** is a lightweight tool designed to simplify the process of labeling data for **Named Entity Recognition (NER)** and allows you to train a model with just a few clicks.

## Features

- Manual or file-based data entry
- Instant model training
- Easy testing and model checkpoint saving

## Installation

To set up the project, run the following command inside your [virtual environment](https://docs.conda.io/projects/conda/en/4.6.0/user-guide/tasks/manage-environments.html)(optional, but recommended):

```bash
pip install -r requirements.txt
```

## Usage

The project provides two ways of adding data: manually or load a json file with a proper format.

1. Manual input: Provide a sentence, the keyword to extract, and its corresponding label
2. Json file: Load a file with the following format:

```
[
{
    "sentence": "The dog is sitting on the ground",
    "word": "dog",
    "label": "ANIMAL"
}
]
```

After adding the data, you can train a model and finally test it. If you need a model for further purposes, it will be in the project folder(use last checkpoint). 

# Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: FastAPI
- Database: MongoDB
- Machine Learning: Hugging Face Transformers

