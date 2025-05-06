#!/usr/bin/env bash
set -o errexit

# Install system dependencies
apt-get update
apt-get install -y tesseract-ocr libmupdf-dev

# Install Python requirements
pip install --upgrade pip
pip install -r requirements.txt
