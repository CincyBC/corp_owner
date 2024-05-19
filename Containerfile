FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    apt-utils \
    python-dev \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./src .

RUN pip install --upgrade pip && pip install --no-cache-dir xgboost==1.7.1 scikit-learn==1.1.3 fastapi==0.111.0 gunicorn==20.1.0 uvicorn==0.29.0

ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["gunicorn", "-w", "3", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]
