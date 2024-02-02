# FROM unit:1.31.1-python3.11
# FROM python:3.9
FROM pytorch/pytorch:2.1.2-cuda11.8-cudnn8-runtime

COPY ./requirements.txt /app/requirements.txt

# RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

# COPY ./config.json /docker-entrypoint.d/config.json


# RUN uvicorn --app-dir /app main:app --host 0.0.0.0 --port 80
CMD ["uvicorn", "main:app", "--host", "192.168.1.5",  "--port", "8000"]


