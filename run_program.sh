#!/bin/bash

# Setting title for the terminal window
echo -e "\033]0;Rescue App Runner\007"

echo ""
echo "=== Rescue Application Launcher ==="
echo ""

# Output current path for debugging
echo "Current path: $(pwd)"
echo ""

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "[ERROR] File requirements.txt not found!"
    echo "Please ensure you're running this script from the project root directory."
    read -p "Press any key to continue..."
    exit 1
fi

# Check for Python installation
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python is not installed or not in PATH."
    echo "Please install Python 3.8+ and try again."
    read -p "Press any key to continue..."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment."
        read -p "Press any key to continue..."
        exit 1
    fi
    echo "Virtual environment created successfully."
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment."
    read -p "Press any key to continue..."
    exit 1
fi

# Install required packages
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[WARNING] Some dependencies might have failed to install."
fi

echo ""
echo "=== Starting Rescue Application ==="
echo ""

# Run the application
echo "Running application..."
python run.py
APP_EXIT_CODE=$?

# Deactivate virtual environment
echo ""
echo "Cleaning up..."
deactivate

if [ $APP_EXIT_CODE -ne 0 ]; then
    echo ""
    echo "[WARNING] Application exited with code $APP_EXIT_CODE"
fi

echo ""
echo "=== Application closed ==="
read -p "Press any key to continue..."
exit $APP_EXIT_CODE 