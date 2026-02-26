FROM python:3.12-slim

WORKDIR /app

# Copy requirements first (Docker caches this layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the source code
COPY . .

# Expose FastAPI Port
EXPOSE 8000

## Start the API
CMD ["python", "-m", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]