#!/bin/bash
echo "Starting Civicosafe Application..."
echo ""
echo "Starting Flask Backend (Terminal 1)..."
gnome-terminal -- bash -c "cd backend && python3 app.py; exec bash" &
sleep 2
echo ""
echo "Starting Frontend Server (Terminal 2)..."
gnome-terminal -- bash -c "cd civicosafe/civicosafe && python3 -m http.server 5500; exec bash" &
sleep 2
echo ""
echo "Both servers are starting!"
echo ""
echo "Open your browser to: http://localhost:5500/login.html"

