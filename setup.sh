#!/bin/bash

# Waifu Animation Chat Setup Script

echo "🎀 Setting up Waifu Animation Chat System..."
echo ""

# Check for pyenv and Python version
if command -v pyenv &> /dev/null; then
    echo "✅ Detected pyenv"
    # Ensure Python 3.11 is available
    if ! pyenv versions | grep -q "3.11"; then
        echo "⚠️  Python 3.11 not found in pyenv"
        echo "   Recommended: pyenv install 3.11.9"
    fi
fi

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.11 (recommended) or higher."
    exit 1
fi

# Show Python version
echo "Python version: $(python3 --version)"
if python3 --version 2>&1 | grep -q "3.1[2-9]\|3.[2-9]"; then
    echo "⚠️  Warning: Python 3.12+ detected. You may experience compatibility issues."
    echo "   Recommended: Use Python 3.11 for best compatibility"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled. Please use Python 3.11"
        exit 1
    fi
fi

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    echo "Please install Node.js 16 or higher."
    exit 1
fi

# Backend setup
echo "📦 Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# Upgrade pip and setuptools first (for Python 3.12 compatibility)
echo "Upgrading pip and setuptools..."
pip install --upgrade pip setuptools wheel

# Install Python dependencies
echo "Installing requirements..."
pip install -r requirements.txt

echo "✅ Backend setup complete!"
echo ""

# Frontend setup
echo "📦 Setting up frontend..."
cd ../frontend

# Clean install to avoid conflicts
echo "🧹 Cleaning node_modules and lock files..."
rm -rf node_modules
rm -f package-lock.json
rm -f yarn.lock

# Clear npm cache
echo "🗑️  Clearing npm cache..."
npm cache clean --force

# Install npm dependencies with legacy peer deps flag to handle version conflicts
echo "Installing frontend dependencies..."
npm install -g yarn
yarn install

echo "✅ Frontend setup complete!"
echo ""

# Create .env file for backend if it doesn't exist
cd ../backend
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOL
# Waifu Animation Chat Configuration

# Server Settings
HOST=0.0.0.0
PORT=8000

# VLLM API Settings (configure when ready)
VLLM_API_URL=http://localhost:8001/v1/completions
VLLM_API_KEY=your-api-key-here
VLLM_MODEL=your-model-name

# Features
ENABLE_VOICE_SYNTHESIS=false
ENABLE_ADVANCED_PHYSICS=true
MAX_AFFECTION_LEVEL=100

# Security
CORS_ORIGINS=["http://localhost:3000"]
EOL
    echo "✅ Created .env file - please configure VLLM settings when ready"
fi

cd ..

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To run the application:"
echo "1. Start the backend: ./run-backend.sh"
echo "2. Start the frontend: ./run-frontend.sh"
echo ""
echo "Or use ./run.sh to start both simultaneously"
