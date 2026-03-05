FROM python:3.12-slim

WORKDIR /app

# Install curl for health check in start.sh
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy requirements first (Docker caches this layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the source code
COPY . .

# Make startup script executable
RUN chmod +x start.sh

# HuggingFace Spaces requires port 7860
EXPOSE 7860

# Set API URL for Streamlit to connect to the local FastAPI
ENV API_URL=http://localhost:8000

# Start both services
CMD ["bash", "start.sh"]