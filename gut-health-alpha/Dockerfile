FROM python:3.11-slim

WORKDIR /app

COPY gut-health-alpha/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY gut-health-alpha/ .

CMD ["python", "-m", "uvicorn", "src.web.api:app", "--host", "0.0.0.0", "--port", "8080"]
