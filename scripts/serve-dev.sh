#!/bin/bash

echo "🚀 STARTING BACKEND AND FRONTEND..."

# Kill any existing processes on ports 3000 and 4200
echo "Cleaning up existing processes..."
taskkill /F /IM node.exe 2>/dev/null || echo "No node processes to kill"

# Build backend
echo "Building backend..."
npx nx run @true-north-audio/backend:build

# Start backend
echo "Starting backend on port 3000..."
NODE_ENV=development node backend/dist/main.js &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start frontend
echo "Starting frontend on port 4200..."
npx nx serve frontend --port=4200 &
FRONTEND_PID=$!

echo "🎉 Services started!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID" 
echo "Frontend: http://localhost:4200"
echo "Backend API: http://localhost:3000/api"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo "Shutting down services..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    exit 0
}

# Set up cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for processes
wait $BACKEND_PID $FRONTEND_PID