#!/bin/bash

echo "=== Testing True North Audio Services ==="
echo ""

# Test Backend
echo -n "Backend (3000): "
if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api | grep -q "200\|404"; then
    echo "✅ Responding"
else
    echo "❌ Not responding"
fi

# Test FastAPI
echo -n "FastAPI (8000): "
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health | grep -q "200"; then
    echo "✅ Responding"
else
    echo "❌ Not responding"
fi

# Test Ollama Proxy
echo -n "Ollama Proxy (11434): "
if curl -s -o /dev/null -w "%{http_code}" http://localhost:11434/health | grep -q "200"; then
    echo "✅ Responding"
else
    echo "❌ Not responding"
fi

# Test Frontend (if running)
echo -n "Frontend (4200): "
if curl -s -o /dev/null -w "%{http_code}" http://localhost:4200 | grep -q "200"; then
    echo "✅ Responding"
else
    echo "❌ Not responding (may not be started yet)"
fi

echo ""
echo "=== Port Status ==="
netstat -ano | grep -E ":(3000|4200|8000|11434).*LISTENING" || echo "No services listening"
