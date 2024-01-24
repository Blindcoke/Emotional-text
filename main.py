from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse, JSONResponse
from transformers import pipeline
import torch
import re
app = FastAPI()

classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None, device=torch.cuda.set_device(0))


class InputSentence(BaseModel):
    text: str

@app.get("/")
async def read_root():
    return FileResponse("index.html")

@app.post("/submit")
async def submit(data: InputSentence):
    try:
        predictions = []
        sentences = re.split(r'(?:\.+ |! |\? )', data.text)
        if not sentences[-1]:
            sentences.pop()
        for i in range(len(sentences)):
            predictions += classifier(sentences[i])
        return JSONResponse(content={"predictions": predictions}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)