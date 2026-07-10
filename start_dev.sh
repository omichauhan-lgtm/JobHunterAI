#!/bin/bash
echo "=========================================="
echo "  STARTING JOBHUNTERAI V12 DEV STACK"
echo "=========================================="
echo ""

# Exit immediately if any command fails, kill background processes on exit
trap "kill 0" EXIT

# Start the Python FastAPI backend server
echo "Starting FastAPI Backend on port 8000..."
python JobHunterAI/api.py &

# Start the Next.js Frontend dev server
echo "Starting Next.js Frontend on port 3000..."
cd frontend && npm run dev &

# Keep script running to print outputs
wait
