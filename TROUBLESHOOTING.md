# Troubleshooting Guide

## Common Issues and Solutions

### Python/Backend Issues

#### ImportError with Python 3.12+
**Solution**: Use Python 3.11 with pyenv
```bash
pyenv install 3.11.9
pyenv local 3.11.9
rm -rf backend/venv
./setup.sh
```

#### vLLM Connection Failed
**Check**:
1. Is vLLM running on erebus:8081?
2. Run `./test-vllm.py` to test connection
3. Check `backend/.env` has correct URL

### Frontend Issues

#### ajv or react-scripts errors
**Solution**: Already fixed by using yarn
```bash
cd frontend
rm -rf node_modules
rm package-lock.json
yarn install
```

#### Images not showing
**Check**:
1. Images are in `frontend/public/models/`
2. Named exactly `luna.jpg` and `sakura.png`
3. Clear browser cache (Ctrl+Shift+R)
4. Check browser console for 404 errors

### WebSocket Issues

#### Chat not connecting
**Check**:
1. Both backend and frontend are running
2. No firewall blocking WebSocket on port 8000
3. Browser console for WebSocket errors

#### Messages not sending
**Check**:
1. vLLM is responding (run `./test-vllm.py`)
2. Backend logs for errors
3. Emotion detection is working

### Performance Issues

#### Slow animations
**Try**:
1. Reduce particle count in WaifuCanvas.js
2. Lower image resolution
3. Disable complex animations

#### High CPU usage
**Try**:
1. Limit frame rate in Three.js
2. Reduce animation complexity
3. Use production build: `cd frontend && yarn build`

## Quick Fixes

### Reset Everything
```bash
# Stop all servers
pkill -f "python.*main.py"
pkill -f "node.*react"

# Clean and rebuild
rm -rf backend/venv
rm -rf frontend/node_modules
./setup.sh
```

### Test Individual Components
```bash
# Test backend only
curl http://localhost:8000/api/models

# Test vLLM
./test-vllm.py

# Check system status
./check-system.sh
```

### Debug Mode

Add to `backend/main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Add to React app:
```javascript
// In App.js
console.log('WebSocket state:', wsRef.current?.readyState);
```

## Still Having Issues?

1. Check all logs in both terminals
2. Look for error messages in browser console
3. Verify all dependencies installed correctly
4. Make sure ports 3000 and 8000 are free
