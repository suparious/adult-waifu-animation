#!/bin/bash
# Quick test script for the Affection System

echo "Testing Affection System Integration..."
echo "======================================"
echo ""

# Check if database module is importable
echo "1. Testing Database Module..."
python3 -c "import sys; sys.path.append('backend'); from database import get_db; print('✅ Database module loaded successfully')" 2>&1

echo ""
echo "2. Testing Affection Manager..."
python3 -c "import sys; sys.path.append('backend'); from affection_manager import get_affection_manager; print('✅ Affection manager loaded successfully')" 2>&1

echo ""
echo "3. Testing Main Integration..."
python3 -c "
import sys
sys.path.append('backend')
try:
    from main import affection_manager
    print('✅ Affection system integrated in main.py')
except Exception as e:
    print(f'❌ Error: {e}')
" 2>&1

echo ""
echo "4. Checking Frontend Components..."
if [ -f "frontend/src/components/AffectionMeter.js" ]; then
    echo "✅ AffectionMeter component exists"
else
    echo "❌ AffectionMeter component missing"
fi

echo ""
echo "5. Testing Quick Affection Calculation..."
python3 -c "
import sys
sys.path.append('backend')
from affection_manager import AffectionManager
am = AffectionManager()
change, reason = am.calculate_affection_change('You are beautiful!', 'happy', {'personality_traits': {'flirtatiousness': 0.8}}, 50)
print(f'✅ Test message: change={change:+d}, reason={reason}')
" 2>&1

echo ""
echo "======================================"
echo "Integration test complete!"
echo ""
echo "To run the full test suite:"
echo "  python test-affection-system.py"
echo ""
echo "To start the application:"
echo "  ./run.sh"
