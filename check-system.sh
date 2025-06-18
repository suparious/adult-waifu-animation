#!/bin/bash

# Quick system check script

echo "🔍 Waifu Animation System Check"
echo "================================"

# Check if backend is running
if curl -s http://localhost:8000 > /dev/null; then
    echo "✅ Backend is running"
    API_RESPONSE=$(curl -s http://localhost:8000)
    echo "   Response: $API_RESPONSE"
else
    echo "❌ Backend is not accessible on port 8000"
fi

echo ""

# Check if frontend is running
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is running"
else
    echo "❌ Frontend is not accessible on port 3000"
fi

echo ""

# Check models endpoint
echo "📋 Available Waifus:"
MODELS=$(curl -s http://localhost:8000/api/models | python3 -m json.tool 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "$MODELS" | grep -E '"name"|"id"' | sed 's/^/   /'
else
    echo "   Could not fetch models"
fi

echo ""

# Check for images
echo "🖼️  Waifu Images:"
for img in frontend/public/models/*; do
    if [ -f "$img" ]; then
        filename=$(basename "$img")
        size=$(ls -lh "$img" | awk '{print $5}')
        echo "   ✅ $filename ($size)"
    fi
done

echo ""
echo "================================"
echo "If everything shows ✅, your system is ready!"
echo "Visit http://localhost:3000 to start chatting!"
