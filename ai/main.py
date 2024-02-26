from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline, RobertaTokenizer
from optimum.onnxruntime import ORTModelForSequenceClassification
import torch
import re
import logging
import io
from typing import Dict
from faster_whisper import WhisperModel
logging.basicConfig(level=logging.DEBUG)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model = WhisperModel("./models/w-base/", device="cuda")
# classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None, device=torch.cuda.set_device(0))
classifier_directory = "./models/onnx/roberta/"
roberta = ORTModelForSequenceClassification.from_pretrained(classifier_directory, file_name="model.onnx")
classifier = pipeline(
    "sentiment-analysis",
    model=roberta,
    tokenizer = RobertaTokenizer.from_pretrained("./models/roberta-base/"),
    top_k=None,
)



class InputSentence(BaseModel):
    text: str
    # audio_file: UploadFile 
    


special_symbols = '(?:\.+ |! |\? |; )'


@app.post("/predict")
async def predict(data: InputSentence):
    try:
        predictions = []
        print(data.text)
        data.text += " "
        symbol_emojies = re.findall(special_symbols, data.text)
        print(symbol_emojies)
        sentences = re.split(special_symbols, data.text)
        if not sentences[-1]:
            sentences.pop()
        for s in sentences:
            predictions += classifier(s)
        logging.info("Predictions: %s", predictions)
        response_data = {
            "predictions": predictions,
            "sentences" : sentences,
            "symbol_emojies" : symbol_emojies
        }
        return JSONResponse(content=response_data , status_code=200)
    except Exception as e:
        logging.error("Error: %s", e)
        return JSONResponse(content={"error": str(e)}, status_code=500)

def transcribe(audio: bytes) -> str:
    segments, _ = model.transcribe(io.BytesIO(audio))
    recognized_text = ''.join([seg.text for seg in list(segments)])
    print(recognized_text)
    return recognized_text

@app.post("/predict")
async def predict(data: InputSentence):
    try:
        predictions = []
        print(data.text)
        data.text += " "
        symbol_emojies = re.findall(special_symbols, data.text)
        print(symbol_emojies)
        sentences = re.split(special_symbols, data.text)
        if not sentences[-1]:
            sentences.pop()
        for s in sentences:
            predictions += classifier(s)
        logging.info("Predictions: %s", predictions)
        response_data = {
            "predictions": predictions,
            "sentences" : sentences,
            "symbol_emojies" : symbol_emojies
        }
        return JSONResponse(content=response_data , status_code=200)
    except Exception as e:
        logging.error("Error: %s", e)
        return JSONResponse(content={"error": str(e)}, status_code=500)




@app.post("/transcribe")
async def transcribe_endpoint(audio: UploadFile) -> Dict[str, str]:
    # try:
    data = ""
    audio_bytes = await audio.read()
    data = transcribe(audio_bytes)
    # print(data)
    data += " "
    predictions = []
    symbol_emojies = re.findall(r'(?:\.+ |! |\? )', data)
    # print(symbol_emojies)
    sentences = re.split(r'(?:\.+ |! |\? |,)', data)
    print(sentences)
    if not sentences[-1]:
        sentences.pop()

    predictions = classifier(sentences)
    logging.info("Predictions: %s", predictions)
    response_data = {
        "predictions": predictions,
        "sentences" : sentences,
        "symbol_emojies" : symbol_emojies
    }
    return JSONResponse(content=response_data, status_code=200)
    # except Exception as e:
    #     logging.error("Error: %s", e)
    #     return JSONResponse(content={"error": str(e)}, status_code=500)




# @app.post("/transcribe")
# async def transcribe_endpoint(audio: UploadFile) -> Dict[str, str]:
#     try:
#         audio_bytes = await audio.read()
#         data = transcribe(audio_bytes)
#         print(data)
#         data += " "
#         predictions = []
#         symbol_emojies = re.findall(r'(?:\.+ |! |\? )', data)
#         print(symbol_emojies)
#         sentences = re.split(r'(?:\.+ |! |\? )', data)
#         if not sentences[-1]:
#             sentences.pop()
#         for i in range(len(sentences)):
#             predictions += classifier(sentences[i])
#         logging.info("Predictions: %s", predictions)
#         response_data = {
#             "predictions": predictions,
#             "sentences" : sentences,
#             "symbol_emojies" : symbol_emojies
#         }
#         return JSONResponse(content=response_data, status_code=200)
#     except Exception as e:
#         logging.error("Error: %s", e)
#         return JSONResponse(content={"error": str(e)}, status_code=500)