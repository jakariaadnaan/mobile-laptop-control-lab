#!/usr/bin/env bash

echo "🚀 Starting Advanced Mobile-Laptop Control Panel..."

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
python3 -m pip install -q psutil paramiko pillow requests 2>/dev/null || true

# Run the app
echo "✅ Dependencies ready. Launching control panel..."
python3 "$(dirname "$0")/app.py"
