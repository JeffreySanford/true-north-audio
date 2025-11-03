# Dockerfile for FastAPI AI music generation service
FROM python:3.11-slim

WORKDIR /app

COPY ai-music-gen/ ./ai-music-gen/
COPY requirements.txt ./
COPY ai-music-gen/requirements.txt ./ai-music-gen/

RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install -r ai-music-gen/requirements.txt \
    && pip install audiocraft ffmpeg-python

EXPOSE 8000

CMD ["uvicorn", "ai-music-gen.musicgen.api:app", "--host", "0.0.0.0", "--port", "8000"]
