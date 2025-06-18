#!/bin/bash

# Make all scripts executable
echo "🔧 Making scripts executable..."
chmod +x *.sh
chmod +x test-vllm.py

echo "✅ Done! All scripts are now executable."
echo ""
echo "Available scripts:"
echo "  ./setup.sh        - Initial setup"
echo "  ./test-vllm.py    - Test vLLM connection"
echo "  ./check-system.sh - Check system status"
echo "  ./run.sh          - Start both servers"
echo "  ./run-backend.sh  - Start backend only"
echo "  ./run-frontend.sh - Start frontend only"
