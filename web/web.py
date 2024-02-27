from fastapi import FastAPI, Request, UploadFile, HTTPException
from fastapi.responses import FileResponse
import requests
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
import os
app = FastAPI()
current_directory = os.path.abspath(os.path.dirname(__file__))
app.mount("/static", StaticFiles(directory=current_directory, html=True), name="static")

@app.get("/")
async def read_root():
    return FileResponse("index.html", media_type='text/html')

class InputSentence(BaseModel):
    text: str

@app.post("/submit")
async def submit(data: InputSentence):
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json={"text": data.text})
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@app.post("/submit_voice")
async def send_voice(audioFile: UploadFile):
    try:
        response  = requests.post(
            "http://127.0.0.1:8000/transcribe",
            files={"audio": audioFile.file.read()},
        )
        print(response.json())
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Middlewares
async def cache_control(request: Request, call_next):
    if request.url.path.startswith("/static"):
        return await call_next(request)
    else:
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-cache, no-store"
        return response


app.add_middleware(BaseHTTPMiddleware, dispatch=cache_control)