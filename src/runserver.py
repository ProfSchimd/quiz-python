import json
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "name": "Quiz Back-end",
        "version": "0.1",
        "author": "Michele Schimd"
    }
    
@app.get("/sample")
def sample_json():
    questions = { 
        "error": "JSON Not Loaded"
    }
    with open(os.path.expanduser("../questions.json")) as fp:
        questions = json.load(fp)
    return questions