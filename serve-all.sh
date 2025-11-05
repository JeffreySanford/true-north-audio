#!/bin/bash

echo "🚀 STARTING ALL SERVICES..."
echo "📡 Services: FastAPI (8000), Ollama API (11434), Backend (3000), Frontend (4200)"

echo "Cleaning up existing processes..."
taskkill /F /IM node.exe 2>/dev/null || echo "No node processes to kill"

echo "Building backend..."
npx nx run @true-north-audio/backend:build

echo "Starting backend on port 3000..."
NODE_ENV=development node backend/dist/main.js &
BACKEND_PID=$!

sleep 5

echo "Starting FastAPI music service..."
pnpm serve:fastapi &
FASTAPI_PID=$!

echo "Starting Ollama proxy (requires Ollama installed)..."
echo "Note: If Ollama is not installed, run: winget install Ollama.Ollama"
pnpm serve:ollama &
OLLAMA_PID=$!

echo "Starting frontend on port 4200..."
npx nx serve frontend --port=4200 --host=0.0.0.0 &
FRONTEND_PID=$!

echo "🎉 All services started! Press Ctrl+C to stop."
echo "Backend PID: $BACKEND_PID"
echo "FastAPI PID: $FASTAPI_PID"
echo "Ollama PID: $OLLAMA_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Frontend: http://localhost:4200"
echo "Backend API: http://localhost:3000/api"
echo "FastAPI: http://localhost:8000"
echo "Ollama: http://localhost:11434"

cleanup() {
	echo "Shutting down services..."
	kill $FRONTEND_PID 2>/dev/null || true
	kill $FASTAPI_PID 2>/dev/null || true
	kill $OLLAMA_PID 2>/dev/null || true
	kill $BACKEND_PID 2>/dev/null || true
	exit 0
}

trap cleanup SIGINT SIGTERM

wait $FASTAPI_PID $OLLAMA_PID $BACKEND_PID $FRONTEND_PID