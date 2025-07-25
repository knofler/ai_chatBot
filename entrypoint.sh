#!/bin/bash
set -e

# Initialize app directories
mkdir -p /app/data
mkdir -p /app/config

# Start the Flask application
cd /app

if [ "$FLASK_ENV" = "development" ]; then
    echo "Starting development server with hot reload..."
    exec flask run --host=0.0.0.0 --port=5000 --debug
else
    echo "Starting production server with Gunicorn..."
    exec gunicorn --bind 0.0.0.0:5000 \
        --workers 4 \
        --timeout 120 \
        --log-level info \
        "src.web_embed_generator:app"
fi
