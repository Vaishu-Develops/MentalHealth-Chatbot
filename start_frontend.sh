#!/bin/bash
# Frontend startup script for Render deployment

# Set the backend URL to the internal service
export BACKEND_URL="https://mindful-companion-backend.onrender.com"

# Start Streamlit on the assigned port
streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true --server.enableCORS false --server.enableXsrfProtection false
