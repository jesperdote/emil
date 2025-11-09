#!/bin/bash

# This script builds and runs the Gmail monitor app using Docker Compose.

# Exit immediately if a command exits with a non-zero status.
set -e

if [ ! -f "credentials.json" ]; then
    echo "------------------------------------------------------------------"
    echo "ERROR: 'credentials.json' not found!"
    echo "Please follow the prerequisite steps to download this file from"
    echo "the Google Cloud Console and place it in this directory."
    echo "------------------------------------------------------------------"
    exit 1
fi

# Ensure token.json exists so Docker can mount it.
touch token.json

echo "Building and starting Docker container..."

# The --build flag ensures the image is rebuilt if the Dockerfile or code changes.
# The -d flag runs it in detached mode (in the background).
docker-compose up --build -d

echo ""
echo "------------------------------------------------------------------"
echo "Application is running inside Docker."
echo "View the UI by navigating to: http://127.0.0.1:5001"
echo ""
echo "To see live logs, run: docker-compose logs -f"
echo "To stop the application, run: docker-compose down"
echo "------------------------------------------------------------------"
