#!/bin/bash

echo "Starting Jhoom Music Bot..."

# Clean up Python cache files
python3 cleanup.py

# Install/upgrade pip
python3 -m pip install --upgrade pip

# Install requirements
python3 -m pip install -U -r requirements.txt

# Run the bot
python3 main.py