#!/bin/bash

# Start FastAPI backend in the background
echo "Starting FastAPI backend on port 8000..."
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &

# Wait for FastAPI to be ready
echo "Waiting for API to start..."
for i in $(seq 1 30); do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "API is ready!"
        break
    fi
    sleep 1
done

# Start Streamlit frontend on port 7860 (HuggingFace default)
echo "Starting Streamlit frontend on port 7860..."
python -m streamlit run src/ui/app.py \
    --server.port=7860 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false
