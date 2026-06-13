#!/bin/bash
echo "==================================================="
echo "  Codex Empower Zero Framework - Mac/Linux Launcher"
echo "==================================================="
echo "Installing dependencies..."

# Check if python3 is available
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    echo "Python is not installed. Please install Python 3.10+ first."
    exit 1
fi

$PIP_CMD install -r requirements.txt

echo ""
echo "Dependencies installed. Launching the application in your browser..."
echo "(Do not close this terminal window)"
echo ""

$PYTHON_CMD -m streamlit run app.py