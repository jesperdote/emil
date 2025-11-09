# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file and install them
# This is done first to leverage Docker's layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY app.py .
COPY templates/ ./templates/

# Expose the port the app runs on
EXPOSE 5001

# Define the command to run your app
# The host is set to 0.0.0.0 to be accessible from outside the container
CMD ["python3", "app.py"]
