#!/bin/bash

# Renovation Client Portal - Development Startup Script
# This script starts both frontend and backend servers

echo "🚀 Starting Renovation Client Portal..."
echo ""

# Check if .env files exist
if [ ! -f "Techhive-frontend/.env" ]; then
    echo "⚠️  Warning: Techhive-frontend/.env not found"
    echo "   Copy .env.example to .env and add your Stripe keys"
    echo ""
fi

if [ ! -f "Renovation/api/.env" ]; then
    echo "⚠️  Warning: Renovation/api/.env not found"
    echo "   Copy .env.example to .env and add your Stripe secret key"
    echo ""
fi

# Check for node_modules
if [ ! -d "Techhive-frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd Techhive-frontend && npm install && cd ..
    echo "✅ Frontend dependencies installed"
    echo ""
fi

# Start backend in background
echo "🔧 Starting Flask backend on port 5000..."
cd Renovation/api
python app.py &
BACKEND_PID=$!
cd ../..

sleep 2

# Start frontend
echo "🎨 Starting Next.js frontend on port 3000..."
cd Techhive-frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Both servers started!"
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
