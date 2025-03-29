#!/bin/bash
# Vintly Run Script for Mac/Unix

echo "Starting Vintly..."

# Check if we're in a virtual environment
if [ -d ".venv" ]; then
    # Try to activate virtual environment
    if [ -f ".venv/bin/activate" ]; then
        echo "Found virtual environment, activating..."
        source .venv/bin/activate
    fi
fi

# Start Flask server in the background and capture PID
python3 app.py > .vintly_output.log 2>&1 &
SERVER_PID=$!

echo "Server starting with PID: $SERVER_PID"

# Monitor log file until server is ready
echo "Waiting for server to start..."
while ! grep -q "Running on" .vintly_output.log; do
    # Check if process is still running
    if ! ps -p $SERVER_PID > /dev/null; then
        echo "[ERROR] Server process died. Check .vintly_output.log for details."
        exit 1
    fi
    sleep 0.5
done

# Extract URL from log file
SERVER_URL=$(grep "Running on" .vintly_output.log | head -n 1 | awk '{print $4}' | sed 's/,$//g')

# Open browser
echo "Server is running! Opening browser at $SERVER_URL"
open $SERVER_URL

echo ""
echo "Vintly is running in the background."
echo "The server log is available in .vintly_output.log"
echo ""
echo "Press Ctrl+C to shut down the server when you're done."

# Handle graceful shutdown on Ctrl+C
trap "echo 'Shutting down Vintly...'; kill $SERVER_PID; rm .vintly_output.log; echo 'Vintly has been shut down.'; exit 0" INT

# Keep script running until Ctrl+C
while true; do
    sleep 1
done