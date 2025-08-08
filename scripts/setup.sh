#!/bin/bash

# setup.sh - Script to set up the environment for the knowledge base

# Install python venv if not already installed
if ! command -v python3 -m venv &> /dev/null; then
    echo "Installing python3-venv..."
    sudo apt-get update
    sudo apt-get install -y python3-venv
fi

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate 

# Install required packages
if [ -f "scripts/requirements.txt" ]; then
    echo "Installing required packages..."
    pip install -r scripts/requirements.txt
fi
