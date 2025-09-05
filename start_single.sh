#!/bin/bash
# Single URL deployment script - runs both backend and frontend

echo "🚀 Starting MindfulCompanion single URL deployment..."

# Start backend API in background
echo "📡 Starting backend API..."
uvicorn backend.api:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 5

# Check if backend is running
if curl -s http://127.0.0.1:8000/health > /dev/null; then
    echo "✅ Backend API is running"
else
    echo "❌ Backend failed to start"
    exit 1
fi

# Start Streamlit frontend on the main port
echo "🎨 Starting frontend..."
export BACKEND_URL="http://127.0.0.1:8000"
streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true --server.enableCORS false --server.enableXsrfProtection false

# If streamlit exits, kill backend
kill $BACKEND_PID
