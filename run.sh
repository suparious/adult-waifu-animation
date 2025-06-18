#!/bin/bash

# Run both backend and frontend with better process management

echo "🎀 Starting Waifu Animation Chat System..."
echo ""

# Function to kill existing processes
cleanup_existing() {
    echo "🧹 Cleaning up any existing processes..."
    
    # Kill any existing backend processes
    pkill -f "python.*main.py" 2>/dev/null
    
    # Kill any existing frontend processes
    pkill -f "node.*react-scripts" 2>/dev/null
    
    # Wait a moment for processes to die
    sleep 2
}

# Function to kill background processes on exit
cleanup() {
    echo ""
    echo "Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    wait $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

# Clean up any existing processes first
cleanup_existing

# Set up cleanup on script exit
trap cleanup EXIT INT TERM

# Start backend in background
echo "Starting backend server..."
cd backend
source venv/bin/activate

# Ensure .env is loaded fresh
export $(grep -v '^#' .env | xargs) 2>/dev/null

python main.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
echo "Waiting for backend to initialize..."
sleep 3

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Backend failed to start! Check the logs above."
    exit 1
fi

# Start frontend in background
echo "Starting frontend server..."
cd frontend
yarn start &
FRONTEND_PID=$!
cd ..

echo ""
echo "✨ Waifu Animation Chat is running!"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for background processes
wait
