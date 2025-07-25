# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Set Python path to include the app directory
ENV PYTHONPATH=/app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install production dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/src/templates /app/src/static

# Copy the application code
COPY src/ /app/src/

# Install development dependencies
RUN if [ "$FLASK_ENV" = "development" ] ; then \
    pip install --no-cache-dir watchdog[watchmedo] ; \
    fi

# Copy the rest of the application
COPY . .

# Create a non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose the port the app runs on
EXPOSE 5000

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Command to run the application
ENTRYPOINT ["/app/entrypoint.sh"]
