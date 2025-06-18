#!/bin/bash

# Run backend server

echo "🚀 Starting Waifu Animation Backend..."
cd backend

# Activate virtual environment
source venv/bin/activate

# Start the FastAPI server
python main.py
