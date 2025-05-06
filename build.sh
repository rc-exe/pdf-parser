#!/usr/bin/env bash
set -o errexit

# Try to install system dependencies (may not work on Render)
if [ -w /var/lib/apt/lists/ ]; then
    sudo apt-get update
    sudo apt-get install -y tesseract-ocr libmupdf-dev
else
    echo "Skipping system package installation (read-only filesystem)"
fi

# Always install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
